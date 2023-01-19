
window.onload = function() {
    // Animacija ucitavanja
    document.querySelector(".loader").style.display = "none";
  };

populateSelect();

// DROPDOWN LISTA S MJESTIMA
function populateSelect() {
    // var XMLHttpRequest = require('xhr2');
    var xhr = new XMLHttpRequest(), 
            method = 'GET',
            overrideMimeType = 'application/json',
            url = './mjesta.json';

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                mjestaFrankopani = JSON.parse(xhr.responseText);
                let ele = document.getElementById('sel');
                for (let i = 0; i < mjestaFrankopani.length; i++) {
                ele.innerHTML = ele.innerHTML +
                    '<option value="' + mjestaFrankopani[i]['ID'] + '">' + mjestaFrankopani[i]['ID'] + '. ' + mjestaFrankopani[i]['Name'] + '</option>';
                }
            }
        };
        xhr.open(method, url, true);
        xhr.send();
}

function show(ele) {
    optIndeks = ele.selectedIndex-1;
    imeMjesta = ele.options[ele.selectedIndex].text
    // console.log(imeMjesta);
    // console.log(optIndeks);
    // console.log(mjestaFrankopani[optIndeks]['Image']);
}


//Globalne varijable
var ticketCounts = {};
var ticketPrices = {};
var total = 0;

var selectedTickets = [];
var total = 0;
var brojac = 0;
document.querySelector('.ticket-count').innerHTML = brojac;		

// Funkcija za plus minus buttons
var btnNumbers = document.querySelectorAll('.btn-number');
for (var i = 0; i < btnNumbers.length; i++) {
    btnNumbers[i].addEventListener('click', function(e) {
        e.preventDefault();
        var fieldName = this.getAttribute('data-field');
        var type = this.getAttribute('data-type');
        var input = document.querySelector("input[name='"+fieldName+"']");
        var ticketBox = this.closest('.ticketBox');
        var ticketPrice = ticketBox.getAttribute('data-ticket-price');
        var ticketType = ticketBox.querySelector('.ticket-name').innerHTML;
        var imeKarte = ticketBox.querySelector('.naslov-karte').innerHTML;
        var currentVal = parseInt(input.value);
        if (!isNaN(currentVal)) {
            if(type == 'minus') {
                brojac -= 1;
                if (brojac <= 0) {
                var cartButtons = document.querySelectorAll('.cart .btn');
                for (var i = 0; i < cartButtons.length; i++) {
                    cartButtons[i].classList.add('disabled');
                }
                }
                if(currentVal > input.getAttribute('min')) {
                    input.value = currentVal - 1;
                    input.dispatchEvent(new Event('change'));
                    updateSelectedTickets(fieldName, imeKarte, ticketPrice, -1);
                } 
                if(parseInt(input.value) == input.getAttribute('min')) {
                    this.setAttribute('disabled', true);
                }
            } else if(type == 'plus') {
                brojac += 1;
                if (brojac > 0) {
                    var cartButtons = document.querySelectorAll('.cart .btn');
                    for (var i = 0; i < cartButtons.length; i++) {
                        cartButtons[i].classList.remove('disabled');
                    }
                }
                if(currentVal < input.getAttribute('max')) {
                    input.value = currentVal + 1;
                    input.dispatchEvent(new Event('change'));
                    updateSelectedTickets(fieldName, imeKarte, ticketPrice, 1);
                }
                if(parseInt(input.value) == input.getAttribute('max')) {
                    this.setAttribute('disabled', true);
                }
            }
        } else {
            input.value = 0;
        }
    });
}


function updateSelectedTickets(fieldName, imeKarte, ticketPrice, count) {
    var found = false;
    
    for(var i = 0; i < selectedTickets.length; i++) {
        if(selectedTickets[i].fieldName === fieldName) {
            selectedTickets[i].count += count;
            found = true;
            if(selectedTickets[i].count === 0) {
                selectedTickets.splice(i, 1);
            }
            break;
        }
    }
    if(!found && count > 0) {
        selectedTickets.push({fieldName: fieldName, ticketType: imeKarte, ticketPrice: ticketPrice, count: count});
    }
    updateTotal();
}

function updateTotal() {
    total = 0;
    for(var i = 0; i < selectedTickets.length; i++) {
        total += selectedTickets[i].ticketPrice * selectedTickets[i].count;
    }
    var ticketCount = document.querySelector('.ticket-count');
    var totalAmount = document.querySelector('.total-amount');
    if(ticketCount){
       ticketCount.innerHTML = brojac;
    }
    if(totalAmount){
        totalAmount.innerHTML = total;
    }
}

var inputNumbers = document.querySelectorAll('.input-number');
for (var i = 0; i < inputNumbers.length; i++) {
    inputNumbers[i].addEventListener('change', function() {
        var minValue = parseInt(this.getAttribute('min'));
        var maxValue = parseInt(this.getAttribute('max'));
        var valueCurrent = parseInt(this.value);
        var name = this.getAttribute('name');
        if(valueCurrent >= minValue) {
            var minusButtons = document.querySelectorAll(".btn-number[data-type='minus'][data-field='"+name+"']");
            for (var i = 0; i < minusButtons.length; i++) {
                minusButtons[i].removeAttribute('disabled');
            }
        } else {
            alert('Najmanja vrijednost dosegnuta!');
            this.value = this.getAttribute('data-oldValue');
        }
        if(valueCurrent <= maxValue) {
            var plusButtons = document.querySelectorAll(".btn-number[data-type='plus'][data-field='"+name+"']");
            for (var i = 0; i < plusButtons.length; i++) {
                plusButtons[i].removeAttribute('disabled');
            }
        } else {
            alert('Najveća vrijednost dosegnuta!');
            this.value = this.getAttribute('data-oldValue');
        }
    });
}

document.querySelector('.view-cart-button').addEventListener('click', function() {
    karteLista = [];
    listaKarta = [];
    if(selectedTickets.length > 0) {
        var kartePopis = document.querySelector('.karte-popis');
        kartePopis.innerHTML = '';
        for(var i = 0; i < selectedTickets.length; i++) {
            // console.log(selectedTickets[i].ticketType);
            var div = document.createElement('div');
            var div1 = document.createElement('div');
            div1.classList.add("kolicina-desno");
            div1.innerHTML = ' x ' + selectedTickets[i].count;
            div.innerHTML = selectedTickets[i].ticketType;
            div.appendChild(div1);
            kartePopis.appendChild(div);
            karteLista.push(selectedTickets[i].ticketType);
            listaKarta.push({
                // id: i+1,
                vrstaKarte: selectedTickets[i].ticketType,
                kolicinaKarte: selectedTickets[i].count,
                cijenaKarte: selectedTickets[i].ticketPrice
            });

        }
        // console.log(karteLista);
        // console.log(listaKarta);
        document.querySelector('.total-amount-2').innerHTML = total + ' €';
        document.querySelector('.datum-odabir').innerHTML = selectedDate;
        document.querySelector('.mjesto-ime').innerHTML = imeMjesta;
        idSlike = mjestaFrankopani[optIndeks]['Image'];
        // console.log(selectedDate + '\n' + total + '\n'  + imeMjesta + '\n'  + mjestaFrankopani[optIndeks]['Image'] + '\n' + optIndeks);
    }
});

const convertImgToBase64URL = (url, callback, outputFormat) => {
    return new Promise((resolve, reject) => {
        let img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = function(){
            let canvas = document.createElement('CANVAS'),
            ctx = canvas.getContext('2d'), dataURL;
            canvas.height = this.height;
            canvas.width = this.width;
            ctx.drawImage(this, 0, 0);
            dataURL = canvas.toDataURL(outputFormat);
            resolve(dataURL);
            canvas = null; 
        };
        img.src = url;
    });
}

// funkcija za pdf racun--------------

const generatePDF = async() => {
    let osobaIme = document.getElementById('forma-ime').value;
    let osobaMail = document.getElementById('forma-mail').value;
    let osobaTel = document.getElementById('forma-telefon').value;
    // console.log('pokrenut pdf');
    // console.log(selectedTickets.length);
    const pdf = new jsPDF();
    pdf.setFontSize(25);
    pdf.setFont("courier", "bold");
    pdf.text('Racun kupljene karte', 10, 10);

    // iznad tablice
    pdf.setFontSize(16);
    pdf.setFont("courier", "normal");
    pdf.text('Ima Kupca: ' + osobaIme, 10, 20);
    pdf.text('Broj Telefona: ' + osobaTel, 10, 30);
    pdf.text('Mail Kupca: ' + osobaMail, 10, 40);
    pdf.text('Datum Posjete: ' + selectedDate, 10, 50);
    pdf.line(10, 55 , 200, 55);
    
    // TABLICA
    pdf.autoTableSetDefaults({
        headStyles: { 
            fillColor: [244, 85, 66],
            fontStyle: 'bold' 
        },
        styles: {
            lineColor: [44, 62, 80],
            lineWidth: 0.5,
            fontSize: 16,
            font: 'courier',
          },
          bodyStyles: {
            textColor: 100,
          },
        })
    var body = listaKarta.map(karta => [karta.vrstaKarte, karta.kolicinaKarte, karta.cijenaKarte, karta.kolicinaKarte * karta.cijenaKarte]);
    pdf.autoTable({
        head: [['Vrsta karte', 'Kolicina', 'Cijena po karti', 'Ukupna cijena']],
        body: body,
        startY: 60,
        theme: 'grid'
    });

    if (total >= 50){
        pdf.setTextColor(244, 85, 66)
        pdf.text('Ostvaren promo kod!', 10, 120);
        pdf.setTextColor(0)
    }

    // ukupno na kraju
    pdf.setFont("courier", "normal");
    pdf.text('Datum Racuna: ' + today, 10, 130);
    pdf.setFont("helvetica", "bold");
    pdf.text('UKUPNO: ' + total + ' €', 10, 140);
    pdf.line(10, 145 , 200, 145);
    let base64Img = await convertImgToBase64URL(idSlike);
    pdf.addImage(base64Img, 'PNG', 10, 170 , 180, 100);
    pdf.save('racunKarte.pdf');
}

const checkoutButton = document.getElementById("checkout-button");
checkoutButton.addEventListener("click", async function(){
    let osobaIme = document.getElementById('forma-ime').value;
    let osobaMail = document.getElementById('forma-mail').value;
    let osobaTel = document.getElementById('forma-telefon').value;
    if (osobaIme && osobaMail && osobaTel){
        await generatePDF();
        window.location.href = "http://localhost:4242/checkout.html";
        createCheckoutSession();
    }
    else {
        alert("Unesite sve podatke");
    }
    
});

// DEFINIRANJE DATUMA
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;
document.getElementById("datepicker").min = today;
today = dd + '-' + mm + '-' + yyyy;

document.getElementById("datepicker").onchange = function(){
    let date = new Date(this.value);
    let dd = String(date.getDate()).padStart(2, '0');
    let mm = String(date.getMonth() + 1).padStart(2, '0'); //sijecanj je 0
    let yyyy = date.getFullYear();
    selectedDate = `${dd}-${mm}-${yyyy}`;
    // console.log(selectedDate);
}