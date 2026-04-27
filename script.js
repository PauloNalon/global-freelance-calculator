function calculate() {
    // 1. Captura os valores dos inputs
    const monthlyTarget = parseFloat(document.getElementById('monthlyValue').value);
    const hoursDay = parseFloat(document.getElementById('hoursPerDay').value);
    const daysOffMonth = parseFloat(document.getElementById('daysOff').value) || 0; 

    // 2. Validação básica (Campos vazios)
    if (!monthlyTarget || !hoursDay) {
        alert("Please, fill in the target value and hours per day!");
        return;
    }

    // 3. Validação Avançada (Impedir dias de folga impossíveis)
    if (daysOffMonth >= 30) {
        const resultElement = document.getElementById('result');
        resultElement.innerText = "Error: Days off exceed a month!";
        resultElement.style.color = "red";
        return; // Para o código aqui se houver erro
    }

    // 4. Lógica do cálculo
    const workingDays = 30 - daysOffMonth;
    const totalHours = workingDays * hoursDay;
    const hourlyRate = monthlyTarget / totalHours;

    // 5. Formatação Internacional (O toque de mestre!)
    const formattedResult = hourlyRate.toLocaleString('en-US', { 
        style: 'currency', 
        currency: 'USD' 
    });

    // 6. Exibe o resultado e reseta a cor para preto (caso estivesse vermelho antes)
    const resultElement = document.getElementById('result');
    resultElement.innerText = `Result: ${formattedResult} / hour`;
    resultElement.style.color = "#333";
}