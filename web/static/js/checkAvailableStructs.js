function main() {
    const refConcs = document.querySelectorAll('.reference-concept-select');
    const compConcs = document.querySelectorAll('.concept-select');

    refConcs.forEach(refConc => {
        const category = refConc.dataset.category;
        const refEntry = document.getElementById(`entry-${category}`);
        if (refEntry) {
            setCombination(refConc, refEntry);
            refConc.addEventListener('change', () => setCombination(refConc, refEntry));
            refEntry.addEventListener('change', () => setCombination(refConc, refEntry));
        }
    });

    compConcs.forEach(compConc => {
        const category = compConc.dataset.category;
        const compEntry1 = document.getElementById(`entry1-${category}`);
        const compEntry2 = document.getElementById(`entry2-${category}`);
        if (compEntry1 && compEntry2) {
            setCombination(compConc, compEntry1, compEntry2);
            compConc.addEventListener('change', () => setCombination(compConc, compEntry1, compEntry2));
            compEntry1.addEventListener('change', () => setCombination(compConc, compEntry1, compEntry2));
            compEntry2.addEventListener('change', () => setCombination(compConc, compEntry1, compEntry2));
        }
    });
}

function getSelectText(selectElem) {
    return selectElem.options[selectElem.selectedIndex].text;
}

function getSelectValue(selectElem) {
    return selectElem.options[selectElem.selectedIndex].value;
}

function setCombination(conc, entry1, entry2=null) {
    const concValue = getSelectValue(conc);
    const entry1Options = entry1.querySelectorAll('option');
    const entry1SelectedOption = entry1.querySelector(`option[value='${getSelectValue(entry1).replace(/'/g, "\\'")}']`);
    const entry1ClassList = entry1SelectedOption ? Array.from(entry1SelectedOption.classList) : [];
    let entry1IsSet = entry1ClassList.includes(concValue);

    for (let i of entry1Options) {
        const classList = Array.from(i.classList);
        if (classList.includes(concValue)) {
            i.disabled = false;
            if (!entry1IsSet) {
                entry1.value = i.value;
                entry1IsSet = true;
            }
        } else {
            i.disabled = true;
        }
    }

    if (entry2 !== null) { 
        const entry2Options = entry2.querySelectorAll('option');
        const entry2SelectedOption = entry2.querySelector(`option[value='${getSelectValue(entry2).replace(/'/g, "\\'")}']`);
        const entry2ClassList = entry2SelectedOption ? Array.from(entry2SelectedOption.classList) : [];
        let entry2IsSet = entry2ClassList.includes(concValue);

        for (let i of entry2Options) {
            const classList = Array.from(i.classList);
            if (classList.includes(concValue)) {
                i.disabled = false;
                if (!entry2IsSet && i.value !== getSelectValue(entry1)) {
                    entry2.value = i.value;
                    entry2IsSet = true;
                }
            } else {
                i.disabled = true;
            }
        }
    }
}



main();
