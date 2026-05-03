async function calculate() {
    const monthlyValue = parseFloat(document.getElementById('monthlyValue').value);
    const hoursPerDay = parseFloat(document.getElementById('hoursPerDay').value);
    const daysOff = parseFloat(document.getElementById('daysOff').value);
    const currency = document.getElementById('currency').value;
    const resultElement = document.getElementById('result');

    // 1. Validação de Erros
    if (isNaN(monthlyValue) || isNaN(hoursPerDay) || isNaN(daysOff)) {
        resultElement.innerText = "Please fill all fields!";
        resultElement.style.color = "red";
        return;
    }

    if (hoursPerDay > 24) {
        resultElement.innerText = "Error: A day only has 24 hours!";
        resultElement.style.color = "red";
        return;
    }

    if (daysOff >= 30) {
        resultElement.innerText = "Error: Days off exceed a month!";
        resultElement.style.color = "red";
        return;
    }

    // 2. Lógica do Cálculo
    const businessDays = 30 - daysOff;
    const totalHoursMonth = businessDays * hoursPerDay;
    const hourlyRate = monthlyValue / totalHoursMonth;

    // 3. Integração com API de Moedas (Opcional, mas muito pro!)
    try {
        // Buscamos a cotação do Dólar e Euro em relação ao Real
        const response = await fetch('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL');
        const data = await response.json();
        
        let rateInBRL = "";
        if (currency === "USD") {
            const brlValue = hourlyRate * data.USDBRL.bid;
            rateInBRL = ` | R$ ${brlValue.toFixed(2)}`;
        } else if (currency === "EUR") {
            const brlValue = hourlyRate * data.EURBRL.bid;
            rateInBRL = ` | R$ ${brlValue.toFixed(2)}`;
        }

        // 4. Exibir Resultado Formatado
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
        });

        resultElement.innerText = `Result: ${formatter.format(hourlyRate)} / hour ${rateInBRL}`;
        resultElement.style.color = "#28a745"; // Verde de sucesso

    } catch (error) {
        // Se a API falhar, mostra o cálculo básico
        resultElement.innerText = `Result: ${currency} ${hourlyRate.toFixed(2)} / hour`;
        console.error("Câmbio indisponível no momento.");
    }
}