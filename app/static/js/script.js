document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/form-data')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(entry => entry.label); // Assuming each entry has a 'label' field

            // Extract values for each of the three experiences
            const values1 = data.map(entry => entry.experience);
            const values2 = data.map(entry => entry.reuse);
            const values3 = data.map(entry => entry.better);

            const ctx = document.getElementById('myChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Experience',
                            data: [values1, values2, values3],
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        },
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});