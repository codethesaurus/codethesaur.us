function main() {
  const refConc = document.getElementById('reference-concept');
  const refLang = document.getElementById('lang');
  const compConc = document.getElementById('concept');
  const compLang1 = document.getElementById('lang1');
  const compLang2 = document.getElementById('lang2');

  // Need to change the value of the second select element
  // in the compare card so that they are not duplicates
  const secondOption = compLang2.querySelectorAll('option')[1];
  compLang2.value = secondOption.value;

  refConc.addEventListener('change', () => handleDomChanges(refConc, refLang));
  refLang.addEventListener('change', () => handleDomChanges(refConc, refLang));
  compConc.addEventListener('change', () => handleDomChanges(compConc, compLang1, compLang2));
  compLang1.addEventListener('change', () => {
    disableDuplicate(compLang1, compLang2);
    handleDomChanges(compConc, compLang1, compLang2)
  });
  compLang2.addEventListener('change', () => {
    disableDuplicate(compLang2, compLang1);
    handleDomChanges(compConc, compLang1, compLang2)
  });

  // Need to check the languages and concepts on the initial load
  disableDuplicate(compLang1, compLang2);
  disableDuplicate(compLang2, compLang1);
  handleDomChanges(refConc, refLang);
  handleDomChanges(compConc, compLang1, compLang2);
}


function disableDuplicate(modifiedSelectElem, unmodifiedSelectElem) {
  const unmodifiedOptionElems = unmodifiedSelectElem.querySelectorAll('option');

  for (let elem of unmodifiedOptionElems) {
    if (elem.disabled == true) {
      elem.disabled = false;
      break;
    }
  }

  const optionElemToDisable = unmodifiedSelectElem.querySelector(`[value="${modifiedSelectElem.value}"]`)
  optionElemToDisable.disabled = true;
}


async function handleDomChanges(concept, langAndVer1, langAndVer2=null) {
  const lang1Value = getSelectValue(langAndVer1);
  const path1 = `/reference/?concept=${getSelectValue(concept)}&lang=${encodeURIComponent(lang1Value)}`;
  const langStatus1 = await doesFileExist(path1).then(data => {return data});
  
  const langAndVer1Text = getSelectText(langAndVer1);
  const conceptText = getSelectText(concept);

  let goBtn, alertDiv, cntrbList;

  if (langAndVer2 === null) {
    goBtn = document.querySelector('[aria-label="Go to reference sheet"]');
    alertDiv = document.getElementById('ref-not-available-alert');
    cntrbList = document.getElementById('ref-github-contribute');

    if (langAndVer2 === null) {
      if (!langStatus1['isAvailable']) {
        handleAlertVisability(alertDiv, changeToHidden=false);
        changeGoButtonStatus(goBtn, enableBtn=false);
        changeAvailabilityText(alertDiv, conceptText, langAndVer1Text);
        changeGithubLinks(cntrbList, concept, langAndVer1);
        changeTemplates(cntrbList, langStatus1['template']);
      }
      else {
        handleAlertVisability(alertDiv, changeToHidden=true);
        changeGoButtonStatus(goBtn, enableBtn=true);
      }
    }
  }
  else {
    goBtn = document.querySelector('[aria-label="Go compare languages"]');
    alertDiv = document.getElementById('comp-not-available-alert');
    cntrbList = document.getElementById('comp-github-contribute');

    const lang2Value = getSelectValue(langAndVer2);
    const path2 = `/reference/?concept=${getSelectValue(concept)}&lang=${encodeURIComponent(lang2Value)}`;
    const langStatus2 = await doesFileExist(path2).then(data => {return data});

    if (langStatus1['isAvailable'] && langStatus2['isAvailable']) {
      handleAlertVisability(alertDiv, changeToHidden=true);
      changeGoButtonStatus(goBtn, enableBtn=true);
    }
    else {
      const langAndVer2Text = getSelectText(langAndVer2);

      if (!langStatus1['isAvailable'] && !langStatus2['isAvailable']) {
        changeAvailabilityText(alertDiv, conceptText, langAndVer1Text, langAndVer2Text);
        changeGithubLinks(cntrbList, concept, langAndVer1, langAndVer2);
        changeTemplates(cntrbList, langStatus1['template'], langStatus2['template']);
      }
      else if (!langStatus1['isAvailable'] && langStatus2['isAvailable']) {
        changeAvailabilityText(alertDiv, conceptText, langAndVer1Text);
        changeGithubLinks(cntrbList, concept, langAndVer1);
        changeTemplates(cntrbList, langStatus1['template']);
      }
      else if (langStatus1['isAvailable'] && !langStatus2['isAvailable']) {
        changeAvailabilityText(alertDiv, conceptText, langAndVer2Text);
        changeGithubLinks(cntrbList, concept, langAndVer2);
        changeTemplates(cntrbList, langStatus2['template']);
      }

      handleAlertVisability(alertDiv, changeToHidden=false);
      changeGoButtonStatus(goBtn, enableBtn=false);
    }
  }
}


function getSelectText(elem) {
  return elem.options[elem.selectedIndex].text;
}


function getSelectValue(elem) {
  return elem.options[elem.selectedIndex].value;
}


async function doesFileExist(urlToFile) {
  try {
    const res =  await fetch(urlToFile);
    if (res.status == 200) {
      return {'isAvailable': true, 'template': null};
    } 
    else if (res.status == 404) {
      const html = await res.text();
      const parser = new DOMParser();
	    const doc = parser.parseFromString(html, 'text/html');
      const detailsElem = doc.querySelector('details');

      return {'isAvailable': false, 'template': detailsElem};
    }
    else {
      throw Error('Unexpected status code in doesFileExist() function');
    }
  }
  catch (error) {
    throw Error(error);
  }
}


function handleAlertVisability(targetElem, changeToHidden) {
  const isHidden = targetElem.classList.contains('visually-hidden');

  if (changeToHidden && !isHidden) {
    targetElem.classList.add('visually-hidden');
  } else if (!changeToHidden && isHidden) {
    targetElem.classList.remove('visually-hidden');
  }
}


function changeGoButtonStatus(btn, enableBtn) {
  if (enableBtn && btn.disabled) {
    btn.disabled = false;
  } else if (!enableBtn && !btn.disabled) {
    btn.disabled = true;
  }
}


function changeAvailabilityText(alertDiv, concept, lang1, lang2=null) {
  const firstPElem = alertDiv.firstElementChild;
  
  if (lang2 === null) {
    firstPElem.textContent = `The "${concept}" concept is not available for "${lang1}"`;
  } else {
    firstPElem.textContent = `The "${concept}" concept is not available for "${lang1}" or "${lang2}"`;
  }
}


function changeGithubLinks(ulElem, concept, langAndVer1, langAndVer2=null) {
  const rootGithubUrl = 'https://github.com/codethesaurus/codethesaur.us/new/main/web/thesauruses';
  const conceptValue = getSelectValue(concept);
  
  const liElem1 = ulElem.firstElementChild;
  const aElem1 = liElem1.querySelector('a');
  
  const lang1Value = getSelectValue(langAndVer1);
  const lang1Text = getSelectText(langAndVer1);
  const lang1 = lang1Value.split(';')[0];
  const ver1 = lang1Value.split(';')[1];

  aElem1.href = `${rootGithubUrl}/${lang1}/${ver1}/${conceptValue}.json?filename=${conceptValue}.json`;
  aElem1.textContent = lang1Text;

  if (ulElem.id === 'comp-github-contribute') {
    const liElem2 = ulElem.lastElementChild;
    const aElem2 = liElem2.querySelector('a');

    if (langAndVer2 === null) {
      aElem2.href = '#';
      aElem2.textContent = '';

      handleAlertVisability(liElem2, changeToHidden=true, changeBtnColor=false);
    }
    else {
      const lang2Value = getSelectValue(langAndVer2);
      const lang2Text = getSelectText(langAndVer2);
      const lang2 = lang2Value.split(';')[0];
      const ver2 = lang2Value.split(';')[1];

      aElem2.href = `${rootGithubUrl}/${lang2}/${ver2}/${conceptValue}.json?filename=${conceptValue}.json`;
      aElem2.textContent = lang2Text;

      handleAlertVisability(liElem2, changeToHidden=false, changeBtnColor=false);
    }
  }
}


function changeTemplates(cntrbList, template1, template2=null) {
  const summary1 = cntrbList.querySelector('summary');
  const textarea1 = cntrbList.querySelector('textarea');

  summary1.textContent = template1.querySelector('summary').textContent;
  textarea1.textContent = template1.querySelector('textarea').textContent;

  if (template2 !== null) {
    const summary2 = cntrbList.lastElementChild.querySelector('summary');
    const textarea2 = cntrbList.lastElementChild.querySelector('textarea');

    summary2.textContent = template2.querySelector('summary').textContent;
    textarea2.textContent = template2.querySelector('textarea').textContent;
  }
}



main();
