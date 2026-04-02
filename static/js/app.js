document.addEventListener("DOMContentLoaded", () => {
    const appShell = document.querySelector(".app-shell");
    const menuToggle = document.getElementById("menuToggle");

    if (appShell && menuToggle) {
        menuToggle.addEventListener("click", () => {
            const current = appShell.getAttribute("data-sidebar-state") || "closed";
            appShell.setAttribute("data-sidebar-state", current === "open" ? "closed" : "open");
        });
    }

    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const submitBtn = form.querySelector("button[type='submit']");
            if (!submitBtn) {
                return;
            }

            submitBtn.dataset.originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = "<span class='spinner-border spinner-border-sm me-2' aria-hidden='true'></span>Processando...";
        });
    });

    document.querySelectorAll("[data-form-stepper]").forEach((stepper) => {
        const panels = Array.from(stepper.querySelectorAll("[data-step-panel]"));
        const chips = Array.from(stepper.querySelectorAll("[data-step-chip]"));
        const nextButtons = Array.from(stepper.querySelectorAll("[data-step-next]"));
        const prevButtons = Array.from(stepper.querySelectorAll("[data-step-prev]"));

        if (!panels.length) {
            return;
        }

        let currentStep = 0;
        const firstErrorStep = panels.findIndex((panel) => panel.querySelector(".text-danger"));
        if (firstErrorStep >= 0) {
            currentStep = firstErrorStep;
        }

        const render = () => {
            panels.forEach((panel, index) => {
                panel.classList.toggle("active", index === currentStep);
            });

            chips.forEach((chip, index) => {
                chip.classList.toggle("active", index === currentStep);
                chip.classList.toggle("done", index < currentStep);
            });
        };

        nextButtons.forEach((button) => {
            button.addEventListener("click", () => {
                if (currentStep < panels.length - 1) {
                    currentStep += 1;
                    render();
                }
            });
        });

        prevButtons.forEach((button) => {
            button.addEventListener("click", () => {
                if (currentStep > 0) {
                    currentStep -= 1;
                    render();
                }
            });
        });

        render();
    });
});
