document.getElementById('cardForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const bankName = document.getElementById('bankName').value;
    const cardHolderName = document.getElementById('cardHolderName').value;
    const cardNumber = document.getElementById('cardNumber').value;
    const expiryDate = document.getElementById('expiryDate').value;
    const cvv = document.getElementById('cvv').value;
    const amount = document.getElementById('amount').value;

    if (!bankName) {
        document.getElementById('result').innerText = "Please select a bank.";
        document.getElementById('result').style.color = "red";
        return;
    }

    // Basic Luhn algorithm check for card validity
    if (!isValidCardNumber(cardNumber)) {
        document.getElementById('result').innerText = "Invalid Card Number. Potential Fraud!";
        document.getElementById('result').style.color = "red";
        return;
    }

    // Basic expiry date check
    if (!isValidExpiryDate(expiryDate)) {
        document.getElementById('result').innerText = "Invalid Expiry Date.";
        document.getElementById('result').style.color = "red";
        return;
    }

    // Basic CVV check
    if (cvv.length !== 3 || isNaN(cvv)) {
        document.getElementById('result').innerText = "Invalid CVV.";
        document.getElementById('result').style.color = "red";
        return;
    }

    // Basic transaction amount check
    if (isNaN(amount) || amount <= 0) {
        document.getElementById('result').innerText = "Invalid Transaction Amount.";
        document.getElementById('result').style.color = "red";
        return;
    }

    document.getElementById('result').innerText = "Card Information is Valid.";
    document.getElementById('result').style.color = "green";
});

function isValidCardNumber(cardNumber) {
    let sum = 0;
    let shouldDouble = false;
    
    for (let i = cardNumber.length - 1; i >= 0; i--) {
        let digit = parseInt(cardNumber[i]);

        if (shouldDouble) {
            if ((digit *= 2) > 9) digit -= 9;
        }

        sum += digit;
        shouldDouble = !shouldDouble;
    }

    return (sum % 10) === 0;
}

function isValidExpiryDate(expiryDate) {
    const [month, year] = expiryDate.split('/');
    if (month < 1 || month > 12) return false;

    const currentYear = new Date().getFullYear() % 100;
    const currentMonth = new Date().getMonth() + 1;

    if (year < currentYear || (year == currentYear && month < currentMonth)) {
        return false;
    }

    return true;
}


