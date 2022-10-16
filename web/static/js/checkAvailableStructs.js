function main() {
    const refConc = document.getElementById('reference-concept');
    const refLang = document.getElementById('lang');
    const compConc = document.getElementById('concept');
    const compLang1 = document.getElementById('lang1');
    const compLang2 = document.getElementById('lang2');
  
    // need to make sure the initial concept and language/version
    // combinations are ones that are available
    setCombination(refConc, refLang);
    setCombination(compConc, compLang1, compLang2);

    refConc.addEventListener('change', () => setCombination(refConc, refLang));
    compConc.addEventListener('change', () => setCombination(compConc, compLang1, compLang2));
}

function getSelectText(selectElem) {
    return selectElem.options[selectElem.selectedIndex].text;
}

function getSelectValue(selectElem) {
    return selectElem.options[selectElem.selectedIndex].value;
}

function setCombination(conc, lang1, lang2=null) {
    const lang1Options = lang1.querySelectorAll('option');
    const lang1ClassList = Array.from(lang1.querySelector(`option[value='${getSelectValue(lang1)}']`).classList);
    let lang1IsSet = lang1ClassList.includes(getSelectValue(conc));

    for (let i of lang1Options) {
        const classList = Array.from(i.classList);
        if (classList.includes(getSelectValue(conc))) {
            if (i.disabled) {
                i.disabled = false;
            }
            if (!lang1IsSet) {
                lang1.value = i.value;
                lang1IsSet = true;
            }
        } else if (!i.disabled) {
            i.disabled = true;
        }
    }

    if (lang2 !== null) { 
        const lang2Options = lang2.querySelectorAll('option');
        const lang2ClassList = Array.from(lang2.querySelector(`option[value='${getSelectValue(lang2)}']`).classList)
        let lang2IsSet = lang2ClassList.includes(getSelectValue(conc));

        for (let i of lang2Options) {
            const classList = Array.from(i.classList);
            if (classList.includes(getSelectValue(conc))) {
                if (i.disabled) {
                    i.disabled = false;
                }
                if (!lang2IsSet && i.value !== getSelectValue(lang1)) {
                    lang2.value = i.value;
                    lang2IsSet = true;
                }
            } else if (!i.disabled) {
                i.disabled = true;
            }
        }
    }
}



main();
