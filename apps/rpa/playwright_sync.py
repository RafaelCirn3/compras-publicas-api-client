import asyncio
import json
import re
from pathlib import Path
from typing import Any

from django.conf import settings
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from apps.filtros.models import FiltroOpcao

TARGET_FIELDS = ["status", "realizacao", "modalidade", "julgamento"]

DROPDOWN_SELECTORS = {
    "status": [".status-dropdown", "[class*='status-dropdown']"],
    "modalidade": [".modalidade-dropdown", "[class*='modalidade-dropdown']"],
    "realizacao": [".realizacao-dropdown", "[class*='realizacao-dropdown']"],
    "julgamento": [".julgamento-dropdown", "[class*='julgamento-dropdown']"],
}

PLACEHOLDER_PATTERNS = [
    re.compile(r"^selecione", re.IGNORECASE),
    re.compile(r"^todos$", re.IGNORECASE),
    re.compile(r"^todas$", re.IGNORECASE),
    re.compile(r"^filtrar", re.IGNORECASE),
]


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def dedup(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in values:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def keep_value(value: str) -> bool:
    if not value:
        return False
    if value.isdigit():
        return False
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(value):
            return False
    return True


async def try_accept_cookies(page) -> None:
    candidates = [
        "button:has-text('Aceitar')",
        "button:has-text('ACEITAR')",
        "button:has-text('Aceitar todos')",
    ]
    for selector in candidates:
        try:
            btn = page.locator(selector).first
            if await btn.count() and await btn.is_visible():
                await btn.click(timeout=1500)
                await page.wait_for_timeout(300)
                return
        except PlaywrightTimeoutError:
            continue


async def open_advanced_filters(page) -> None:
    triggers = [
        "button:has-text('Busca Avançada')",
        "a:has-text('Busca Avançada')",
        "text=Busca Avançada",
    ]
    for selector in triggers:
        try:
            target = page.locator(selector).first
            if await target.count() and await target.is_visible():
                await target.click(timeout=3000)
                await page.wait_for_timeout(900)
                return
        except PlaywrightTimeoutError:
            continue


async def collect_visible_options_text(page) -> list[str]:
    values: list[str] = []
    locators = [
        page.locator(".dropdown-list li, .dropdown-list button, .dropdown-list [role='option']"),
        page.locator("[role='listbox'] [role='option'], [role='option']"),
    ]
    for locator in locators:
        count = await locator.count()
        for idx in range(count):
            text = clean_text(await locator.nth(idx).inner_text())
            if keep_value(text):
                values.append(text)
    return dedup(values)


async def scroll_open_dropdown_and_collect(page) -> list[str]:
    script = """
() => {
  const candidates = Array.from(document.querySelectorAll('.dropdown-list, [role="listbox"], .cdk-virtual-scroll-viewport'));
  const visible = candidates.find(el => {
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  });
  if (!visible) return {ok:false};
  visible.scrollTop = visible.scrollTop + Math.max(visible.clientHeight * 0.8, 120);
  return {
    ok: true,
    top: visible.scrollTop,
    height: visible.scrollHeight,
    client: visible.clientHeight
  };
}
"""
    all_values: list[str] = []
    last_signature = ""
    stable_loops = 0

    for _ in range(40):
        all_values.extend(await collect_visible_options_text(page))
        state = await page.evaluate(script)
        if not state or not state.get("ok"):
            break
        await page.wait_for_timeout(180)
        signature = f"{state.get('top')}|{state.get('height')}|{len(dedup(all_values))}"
        if signature == last_signature:
            stable_loops += 1
        else:
            stable_loops = 0
        last_signature = signature

        reached_end = state.get("top", 0) + state.get("client", 0) >= state.get("height", 0) - 4
        if reached_end and stable_loops >= 2:
            break

    return dedup(all_values)


async def collect_dropdown_from_dom(page, field: str) -> list[str]:
    selectors = DROPDOWN_SELECTORS.get(field, [])
    values: list[str] = []

    for root_selector in selectors:
        root = page.locator(root_selector).first
        if await root.count() == 0:
            continue

        button = root.locator(".dropdown-btn, button").first
        if await button.count() == 0:
            continue

        try:
            await button.click(timeout=2500)
            await page.wait_for_timeout(500)
        except PlaywrightTimeoutError:
            continue

        values.extend(await collect_visible_options_text(page))
        values.extend(await scroll_open_dropdown_and_collect(page))

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(200)

    return dedup(values)


async def _run(url: str, html_output: Path, json_output: Path, headless: bool = True) -> dict[str, Any]:
    data: dict[str, Any] = {
        "url": url,
        "campos": {field: [] for field in TARGET_FIELDS},
        "observacoes": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(locale="pt-BR")
        page = await context.new_page()

        await page.goto(url, wait_until="domcontentloaded", timeout=90000)
        await try_accept_cookies(page)
        await open_advanced_filters(page)
        await page.wait_for_timeout(2500)

        html = await page.content()
        html_output.write_text(html, encoding="utf-8")

        for field in DROPDOWN_SELECTORS:
            data["campos"][field] = await collect_dropdown_from_dom(page, field)

        for field, values in data["campos"].items():
            data["campos"][field] = dedup([clean_text(v) for v in values if keep_value(clean_text(v))])

        await browser.close()

    json_output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def executar_extracao_filtros(
    url: str = "https://www.portaldecompraspublicas.com.br/processos",
    headless: bool = True,
    html_output: str = "portal_processos_renderizado.html",
    json_output: str = "filtros_dropdown.json",
) -> dict[str, Any]:
    export_dir = Path(settings.BASE_DIR) / "exports"
    export_dir.mkdir(exist_ok=True)
    html_path = export_dir / html_output
    json_path = export_dir / json_output

    return asyncio.run(
        _run(
            url=url,
            html_output=html_path,
            json_output=json_path,
            headless=headless,
        )
    )


def sincronizar_filtros_dropdown(url: str = "https://www.portaldecompraspublicas.com.br/processos", headless: bool = True) -> dict[str, int]:
    data = executar_extracao_filtros(url=url, headless=headless)

    criados = 0
    atualizados = 0
    for campo, valores in data.get("campos", {}).items():
        if campo not in TARGET_FIELDS:
            continue
        FiltroOpcao.objects.filter(campo=campo).delete()
        for valor in valores:
            FiltroOpcao.objects.create(campo=campo, valor=valor)
            criados += 1

    return {"total_criados": criados, "total_atualizados": atualizados}
