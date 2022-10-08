function main() {
    const refConc = document.getElementById('reference-concept');
    const refLang = document.getElementById('lang');
    const compConc = document.getElementById('concept');
    const compLang1 = document.getElementById('lang1');
    const compLang2 = document.getElementById('lang2');
  
    // need to make sure the initial language(s) and concept
    // combination is one that is available
    setInitialCombination(refConc, refLang);
    setInitialCombination(compConc, compLang1, compLang2);
    
    disableOptions(refConc, refLang);
    disableOptions(compConc, compLang1, compLang2);

    refConc.addEventListener('change', () => disableOptions(refConc, refLang));
    refLang.addEventListener('change', () => disableOptions(refConc, refLang));
    compConc.addEventListener('change', () => disableOptions(compConc, compLang1, compLang2));
    compLang1.addEventListener('change', () => disableOptions(compConc, compLang1, compLang2));
    compLang2.addEventListener('change', () => disableOptions(compConc, compLang1, compLang2));
}

function getSelectText(selectElem) {
    return selectElem.options[selectElem.selectedIndex].text;
}

function getSelectValue(selectElem) {
    return selectElem.options[selectElem.selectedIndex].value;
}

function setInitialCombination(conc, lang1, lang2=null) {
    const concOptions = conc.querySelectorAll('option');
    const lang1Options = lang1.querySelectorAll('option');

    if (lang2 === null) {
        for (let i = 0; i < lang1Options.length - 1; i++) {
            const lang1ClassList = Array.from(lang1[i].classList);

            for (let k = 0; k < concOptions.length; k++) {
                if (lang1ClassList.includes(concOptions[k].value)) {
                    conc.value = concOptions[k].value;
                    lang1.value = lang1Options[i].value;
                    return;
                } 
            }
        }
    } else {
        const lang2Options = lang2.querySelectorAll('option');

        for (let i = 0; i < lang1Options.length - 1; i++) {
            const lang1ClassList = Array.from(lang1[i].classList);

            for (let j = i + 1; j < lang2Options.length; j++) {
                const lang2ClassList = Array.from(lang2[j].classList);

                for (let k = 0; k < concOptions.length; k++) {
                    if (lang1ClassList.includes(concOptions[k].value) && lang2ClassList.includes(concOptions[k].value)) {
                        conc.value = concOptions[k].value;
                        lang1.value = lang1Options[i].value;
                        lang2.value = lang2Options[j].value;
                        return;
                    } 
                }
            }
        }
    }
}

function disableOptions(conc, lang1, lang2=null) {
    const concOptions = conc.querySelectorAll('option');
    const lang1Options = lang1.querySelectorAll('option');
    const lang1SelectedOption = document.querySelector(`select#${lang1.id} option[value='${getSelectValue(lang1)}']`);
    const lang1ClassList = Array.from(lang1SelectedOption.classList);

    
    if (lang2 === null) {
        for (let i of concOptions) {
            if (lang1ClassList.includes(i.value) && i.disabled) {
                i.disabled = false;
            } else if (!lang1ClassList.includes(i.value) && !i.disabled) {
                i.disabled = true;
            }
        }
        for (let i of lang1Options) {
            if (Array.from(i.classList).includes(getSelectValue(conc)) && i.disabled) {
                i.disabled = false;
            } else if (!Array.from(i.classList).includes(getSelectValue(conc)) && !i.disabled) {
                i.disabled = true;
            }
        }
    } else {
        const lang2Options = lang2.querySelectorAll('option');
        const lang2SelectedOption = document.querySelector(`select#${lang2.id} option[value='${getSelectValue(lang2)}']`);
        const lang2ClassList = Array.from(lang2SelectedOption.classList);

        for (let i of concOptions) {
            if (lang1ClassList.includes(i.value) && lang2ClassList.includes(i.value) && i.disabled) {
                i.disabled = false;
            } else if ((!lang1ClassList.includes(i.value) || !lang2ClassList.includes(i.value)) && !i.disabled) {
                i.disabled = true;
            }
        }
        for (let i of lang1Options) {
            if (Array.from(i.classList).includes(getSelectValue(conc)) && i.disabled) {
                i.disabled = false;
            } else if (!Array.from(i.classList).includes(getSelectValue(conc)) && !i.disabled) {
                i.disabled = true;
            }
        }
        for (let i of lang2Options) {
            if (Array.from(i.classList).includes(getSelectValue(conc)) && i.disabled) {
                i.disabled = false;
            } else if (!Array.from(i.classList).includes(getSelectValue(conc)) && !i.disabled) {
                i.disabled = true;
            }
        }
    }
}



main();
