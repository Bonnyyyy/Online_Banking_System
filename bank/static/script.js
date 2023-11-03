document.addEventListener("DOMContentLoaded", () => {
    const backButton = document.getElementById("back");
    const transferForm = document.getElementById("transfer-form");

    backButton.addEventListener("click", () => {
        // Simulate going back to the dashboard
        window.location.href = "dashboard.html";
    });

    transferForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const fromAccount = document.getElementById("from-account").value;
        const toAccount = document.getElementById("to-account").value;
        const amount = parseFloat(document.getElementById("amount").value);

        if (isNaN(amount) || amount <= 0) {
            alert("Please enter a valid amount.");
            return;
        }

        // Simulate processing the transfer (update account balances, etc.)
        alert(`Transferred $${amount} from account ${fromAccount} to account ${toAccount}.`);
        transferForm.reset();
    });
});
