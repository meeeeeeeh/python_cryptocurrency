const c1 = document.getElementById("currency-one");
const c2 = document.getElementById("currency-two");
const amount1 = document.getElementById("amount-one");
const amount2 = document.getElementById("amount-two");
const theRate = document.getElementById("rate");
const exchange = document.getElementById("exchange");

c1.addEventListener('change', calculate);
amount1.addEventListener('input', calculate);
c2.addEventListener('change', calculate);
amount2.addEventListener('input', calculate);

exchange.addEventListener('click', () => {
    const temp = c1.value;
    c1.value = c2.value;
    c2.value = temp;
    calculate();
});

function calculate() {
    const curr1 = c1.value;
    const curr2 = c2.value;
    fetch(`https://api.exchangerate-api.com/v4/latest/${curr1}`)
        .then(res => res.json())
        .then(res => {
            const exRate = res.rates[curr2];
            theRate.innerText = `1 ${curr1} = ${exRate} ${curr2}`
            amount2.value = (amount1.value * exRate).toFixed(2);
        });
};

calculate();

