(function(){
  var burger=document.querySelector('.burger'),menu=document.getElementById('menu'),toast=document.getElementById('toast'),tt;
  function say(t){if(!toast)return;toast.textContent=t;toast.classList.add('show');clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove('show')},2600)}
  function setMenu(o){menu.classList.toggle('open',o);burger.setAttribute('aria-expanded',String(o));burger.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')}
  if(burger&&menu){
    burger.addEventListener('click',function(){setMenu(!menu.classList.contains('open'))});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu.classList.contains('open')){setMenu(false);burger.focus()}});
    menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
    window.addEventListener('resize',function(){if(window.innerWidth>980)setMenu(false)});
  }
  function copyText(v,line,okMsg){
    function fb(){
      var el=line;if(!el)return;
      if(el.select){el.focus();el.select()}else{var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}
      say('Sélectionné : copiez avec Ctrl+C')}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v).then(function(){say(okMsg)},fb)}else fb();
  }
  document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
    copyText(b.dataset.copy,b.parentNode.querySelector('span'),'Copié : '+b.dataset.copy)})});

  /* Formulaire de contact */
  var form=document.getElementById('devis');
  if(!form)return;
  var PHONE='+33612779171',MAIL='a.e.p.s.dujardin@gmail.com';
  var recap=document.getElementById('recap'),txt=document.getElementById('recap-text');
  function f(id){return document.getElementById(id)}
  function setErr(id,msg){var i=f(id),e=f(id+'-err');if(msg){i.setAttribute('aria-invalid','true');e.textContent=msg}else{i.removeAttribute('aria-invalid');e.textContent=''}return !msg}
  function check(){
    var ok=true,first=null;
    function chk(id,msg){var good=setErr(id,msg);if(!good&&!first)first=f(id);ok=ok&&good}
    var nom=f('nom').value.trim(),tel=f('tel').value.trim(),mail=f('mail').value.trim(),type=f('type').value,msg=f('msg').value.trim();
    chk('nom',nom.length<2?'Indiquez votre nom.':'');
    chk('tel',!tel?'Indiquez un numéro de téléphone.':(/^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.\-]*\d{2}){4}$/.test(tel)?'':'Numéro invalide. Exemple : 06 12 34 56 78.'));
    chk('mail',mail&&!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)?'Adresse e-mail invalide. Exemple : nom@exemple.fr':'');
    chk('type',!type?'Choisissez le type de projet.':'');
    chk('msg',msg.length<10?'Décrivez votre projet en quelques mots (10 caractères minimum).':'');
    if(first)first.focus();
    return ok;
  }
  form.addEventListener('submit',function(e){
    e.preventDefault();
    if(!check()){recap.hidden=true;return}
    var lines=['Bonjour, je souhaite un devis pour : '+f('type').value+'.','',
      'Nom : '+f('nom').value.trim(),'Téléphone : '+f('tel').value.trim()];
    if(f('mail').value.trim())lines.push('E-mail : '+f('mail').value.trim());
    if(f('commune').value.trim())lines.push('Commune : '+f('commune').value.trim());
    lines.push('','Projet : '+f('msg').value.trim());
    var text=lines.join('\n');
    txt.value=text;
    document.getElementById('sms').href='sms:'+PHONE+'?&body='+encodeURIComponent(text);
    document.getElementById('mailto').href='mailto:'+MAIL+'?subject='+encodeURIComponent('Demande de devis paysage')+'&body='+encodeURIComponent(text);
    recap.hidden=false;
    document.getElementById('recap-title').focus();
    recap.scrollIntoView({behavior:'smooth',block:'start'});
  });
  ['nom','tel','mail','type','msg'].forEach(function(id){f(id).addEventListener('input',function(){if(f(id).getAttribute('aria-invalid'))check()})});
  document.getElementById('copier').addEventListener('click',function(){copyText(txt.value,txt,'Message copié')});
  document.getElementById('modifier').addEventListener('click',function(){recap.hidden=true;f('nom').focus()});
})();
