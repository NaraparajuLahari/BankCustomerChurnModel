document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("churnForm").addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        // Collect form data
        let formData = {
            CreditScore: parseInt(document.getElementById("credit_score").value),
            Age: parseInt(document.getElementById("age").value),
            Tenure: parseInt(document.getElementById("tenure").value),
            Balance: parseFloat(document.getElementById("balance").value),
            NumOfProducts: parseInt(document.getElementById("num_products").value),
            HasCrCard: parseInt(document.getElementById("has_cr_card").value),
            IsActiveMember: parseInt(document.getElementById("is_active_member").value),
            EstimatedSalary: parseFloat(document.getElementById("estimated_salary").value),
            CustomerFeedback: parseInt(document.getElementById("customer_feedback").value)
        };

        try {
            let response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },  // Send as JSON
                body: JSON.stringify(formData)
            });

            let result = await response.json(); // Parse JSON response

            if (result.error) {
                document.getElementById("result").innerText = "Error: " + result.error;
            } else {
                document.getElementById("result").innerText = "Churn Prediction: " + (result.churn ? "Yes" : "No");

                // Show the graph if available
                if (result.graph_url) {
                    let graph = document.getElementById("graph");
                    graph.src = result.graph_url;
                    graph.style.display = "block"; // Make the graph visible
                }
            }
        } catch (error) {
            document.getElementById("result").innerText = "Error: Unable to connect to server.";
        }
    });
});
