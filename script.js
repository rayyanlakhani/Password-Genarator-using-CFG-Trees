document.getElementById("generate-btn").addEventListener("click", async () => {
  const phrase = document.getElementById("phrase").value;

  if (!phrase) {
    alert("Please enter a phrase!");
    return;
  }

  // Send the phrase to the backend
  try {
    const response = await fetch("http://127.0.0.1:5000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phrase }),
    });

    const data = await response.json();

    if (response.ok) {
      // Display the generated password
      document.getElementById("password-output").textContent = data.password;
    } else {
      alert(data.error || "An error occurred");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to connect to the server.");
  }
});
