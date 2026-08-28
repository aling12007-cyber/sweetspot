from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = {
    'en:"Rights holders"': 'en:"Rights Holders"',
    'en:"Elite athletes"': 'en:"Elite Athletes"',
    'en:"baseball, cricket, golf, football, Formula One, rugby, and tennis."': 'en:"Baseball, cricket, golf, football, Formula One, rugby, and tennis."',
    'en:"finance, payment services, sportswear, tech & wearables."': 'en:"Finance, payment services, sportswear, tech & wearables."',
    'en:"active and retired."': 'en:"Active and retired."',
}
for old, new in replacements.items():
    text = text.replace(old, new)

for marker in [
    '/* Broad Influence cards — distinct premium treatments */',
    '/* Broad Influence cards — screenshot reference composition */'
]:
    if marker in text:
        start = text.index(marker)
        end = text.index('</style>', start)
        text = text[:start] + text[end:]
        break

css = r'''/* Broad Influence cards — screenshot reference composition */
#network .network-grid{gap:18px!important;border:0!important;background:none!important}
#network .network-grid article{position:relative!important;isolation:isolate;overflow:hidden!important;min-height:228px!important;padding:28px 28px 26px!important;border:1px solid rgba(255,255,255,.15)!important;background:#0b121b!important;box-shadow:0 14px 36px rgba(0,0,0,.18),inset 0 1px 0 rgba(255,255,255,.025)!important;transition:transform .28s ease,border-color .28s ease,box-shadow .28s ease!important}
#network .network-grid article>*{position:relative;z-index:3}
#network .network-grid .network-icon{display:grid!important;place-items:center!important;width:64px!important;height:64px!important;margin:0!important;border:1px solid rgba(215,169,54,.62)!important;border-radius:50%!important;color:#f1d36d!important;background:rgba(8,13,20,.48)!important;box-shadow:none!important;font-size:15px!important;font-weight:900!important}
#network .network-grid h3{margin:26px 0 12px!important;max-width:56%;color:#fff!important;font-size:clamp(25px,2.15vw,32px)!important;font-weight:800!important;line-height:1.08!important;letter-spacing:-.025em!important}
#network .network-grid p{margin:0!important;max-width:58%;color:#c0c8d3!important;font-size:15px!important;line-height:1.58!important}
#network .network-grid article:hover{transform:translateY(-3px)!important;box-shadow:0 20px 46px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.035)!important}

#network .network-grid article:nth-child(1){border-color:rgba(215,169,54,.5)!important;border-radius:20px 20px 0 0!important;background:radial-gradient(circle at 78% 72%,rgba(215,169,54,.08),transparent 32%),linear-gradient(135deg,#111b28 0%,#0b121b 66%,#091019 100%)!important}
#network .network-grid article:nth-child(1):before{content:"";position:absolute;z-index:1;right:2%;bottom:-7%;width:54%;height:78%;opacity:.34;background-repeat:no-repeat;background-position:right bottom;background-size:contain;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 420 260'%3E%3Cg fill='%238b97a6'%3E%3Cpath d='M70 214h280v18H70z'/%3E%3Cpath d='M92 192h236v22H92z'/%3E%3Cpath d='M116 92h188v100H116z' opacity='.72'/%3E%3Cpath d='M104 92h212L210 30 104 92z'/%3E%3Cpath d='M188 20h44v16h-44z'/%3E%3Cpath d='M198 4h24v18h-24z'/%3E%3Cpath d='M134 105h20v78h-20zM170 105h20v78h-20zM206 105h20v78h-20zM242 105h20v78h-20zM278 105h20v78h-20z' fill='%235f6b79'/%3E%3Cpath d='M50 216h320v10H50z'/%3E%3C/g%3E%3C/svg%3E")}
#network .network-grid article:nth-child(1):after{content:"";position:absolute;z-index:2;right:-10%;bottom:-44%;width:62%;aspect-ratio:1;border:1px solid rgba(215,169,54,.58);border-radius:50%;box-shadow:0 0 18px rgba(215,169,54,.09)}

#network .network-grid article:nth-child(2){clip-path:polygon(20px 0,calc(100% - 18px) 0,100% 18px,100% calc(100% - 18px),calc(100% - 18px) 100%,18px 100%,0 calc(100% - 18px),0 18px)!important;border-color:rgba(255,255,255,.16)!important;background:linear-gradient(145deg,rgba(215,169,54,.035),transparent 28%),linear-gradient(135deg,#111923 0%,#0a1119 72%)!important}
#network .network-grid article:nth-child(2):before{content:"";position:absolute;z-index:1;right:4%;top:21%;width:43%;height:58%;opacity:.88;background-repeat:no-repeat;background-position:center;background-size:contain;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 180' fill='none' stroke='%23d7a936' stroke-width='3'%3E%3Ccircle cx='55' cy='48' r='28'/%3E%3Cpath d='M42 25c10 12 10 34 0 46M68 25c-10 12-10 34 0 46'/%3E%3Ccircle cx='142' cy='48' r='28'/%3E%3Cpath d='M125 67l34-38M131 72l34-38'/%3E%3Ccircle cx='230' cy='48' r='28'/%3E%3Ccircle cx='230' cy='48' r='13' stroke-dasharray='2 5'/%3E%3Cpath d='M230 76v18M215 94h30'/%3E%3Ccircle cx='72' cy='132' r='26'/%3E%3Cpath d='M56 120l16-10 16 10-6 19H62zM56 120l-11 6 3 15 14 8M88 120l11 6-3 15-14 8M72 110v-10'/%3E%3Cpath d='M142 108v48M142 110l28 10-28 10'/%3E%3Cpath d='M219 108c17 0 29 11 29 24s-12 24-29 24-29-11-29-24 12-24 29-24z'/%3E%3Cpath d='M203 142l32-20'/%3E%3Ccircle cx='316' cy='132' r='25'/%3E%3Cpath d='M297 113c17 12 17 26 0 38M335 113c-17 12-17 26 0 38'/%3E%3C/svg%3E")}
#network .network-grid article:nth-child(2):after{content:"";position:absolute;z-index:0;right:0;top:0;width:47%;height:100%;opacity:.22;background:linear-gradient(30deg,transparent 24%,rgba(215,169,54,.08) 25% 26%,transparent 27% 74%,rgba(215,169,54,.08) 75% 76%,transparent 77%),linear-gradient(150deg,transparent 24%,rgba(215,169,54,.08) 25% 26%,transparent 27% 74%,rgba(215,169,54,.08) 75% 76%,transparent 77%);background-size:34px 58px;-webkit-mask-image:linear-gradient(90deg,transparent,#000);mask-image:linear-gradient(90deg,transparent,#000)}

#network .network-grid article:nth-child(3){border-color:rgba(215,169,54,.56)!important;border-radius:0 8px 0 8px!important;background:radial-gradient(circle at 83% 44%,rgba(215,169,54,.1),transparent 27%),linear-gradient(145deg,#101720,#0b1017 72%)!important}
#network .network-grid article:nth-child(3):before{content:"";position:absolute;z-index:1;right:-2%;top:3%;width:46%;aspect-ratio:1;border-radius:50%;background-image:radial-gradient(circle,rgba(244,207,89,.82) 0 1.2px,transparent 1.5px);background-size:11px 11px;opacity:.58;transform:rotate(-8deg);box-shadow:-12px 0 26px rgba(215,169,54,.12),inset 14px 0 34px rgba(0,0,0,.24);-webkit-mask-image:radial-gradient(circle at 35% 50%,#000 0 62%,transparent 70%);mask-image:radial-gradient(circle at 35% 50%,#000 0 62%,transparent 70%)}
#network .network-grid article:nth-child(3):after{content:"";position:absolute;z-index:2;right:5%;top:9%;width:42%;aspect-ratio:1;border-left:1px solid rgba(255,218,95,.8);border-radius:50%;filter:drop-shadow(0 0 6px rgba(255,212,76,.38))}
#network .network-grid article:nth-child(3) h3,#network .network-grid article:nth-child(3) p{max-width:50%}

#network .network-grid article:nth-child(4){border-left:3px solid var(--gold)!important;border-radius:18px 0 18px 0!important;background:radial-gradient(circle at 83% 48%,rgba(215,169,54,.08),transparent 28%),linear-gradient(145deg,#0d131b,#090e14 78%)!important}
#network .network-grid article:nth-child(4):before{content:"";position:absolute;z-index:1;right:4%;top:21%;width:44%;height:60%;opacity:.92;background-repeat:no-repeat;background-position:center;background-size:contain;filter:drop-shadow(0 0 7px rgba(215,169,54,.2));background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 340 170'%3E%3Cg fill='none' stroke='%23d7a936' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='233' cy='34' r='12' fill='%23d7a936'/%3E%3Cpath d='M220 48l-28 24 30 18 24-24 22 10'/%3E%3Cpath d='M194 74l-38 16 24 9'/%3E%3Cpath d='M220 90l-30 28-37 28M222 90l38 20 35 30'/%3E%3Cpath d='M153 146l-22 5M295 140l21 7'/%3E%3C/g%3E%3Cg stroke='%23d7a936' stroke-width='2' opacity='.45'%3E%3Cpath d='M70 58h112M45 74h120M26 90h128M52 106h99M85 122h65'/%3E%3C/g%3E%3Cg fill='%23d7a936' opacity='.75'%3E%3Ccircle cx='205' cy='66' r='2'/%3E%3Ccircle cx='212' cy='61' r='2'/%3E%3Ccircle cx='218' cy='56' r='2'/%3E%3Ccircle cx='225' cy='52' r='1.8'/%3E%3Ccircle cx='189' cy='88' r='1.8'/%3E%3Ccircle cx='179' cy='92' r='1.8'/%3E%3Ccircle cx='169' cy='96' r='1.6'/%3E%3C/g%3E%3C/svg%3E")}
#network .network-grid article:nth-child(4):after{content:"";position:absolute;z-index:0;right:4%;top:31%;width:48%;height:38%;opacity:.34;background:repeating-linear-gradient(0deg,transparent 0 8px,rgba(215,169,54,.26) 8px 9px);-webkit-mask-image:linear-gradient(90deg,transparent,#000 40%,transparent);mask-image:linear-gradient(90deg,transparent,#000 40%,transparent)}
#network .network-grid article:nth-child(4) h3,#network .network-grid article:nth-child(4) p{max-width:50%}

@media(max-width:760px){
  #network .network-grid{gap:18px!important}
  #network .network-grid article{min-height:262px!important;padding:26px 26px 24px!important}
  #network .network-grid .network-icon{width:58px!important;height:58px!important;font-size:14px!important}
  #network .network-grid h3{margin:28px 0 12px!important;max-width:58%!important;font-size:clamp(28px,7.2vw,32px)!important}
  #network .network-grid p{max-width:58%!important;font-size:16px!important;line-height:1.52!important}
  #network .network-grid article:nth-child(1){min-height:292px!important}
  #network .network-grid article:nth-child(1):before{right:-2%;bottom:-3%;width:55%;height:72%;opacity:.3}
  #network .network-grid article:nth-child(1):after{right:-18%;bottom:-42%;width:68%}
  #network .network-grid article:nth-child(2):before{right:1%;top:23%;width:46%;height:55%}
  #network .network-grid article:nth-child(3){min-height:252px!important}
  #network .network-grid article:nth-child(3):before{right:-11%;top:3%;width:58%}
  #network .network-grid article:nth-child(3):after{right:-4%;top:9%;width:54%}
  #network .network-grid article:nth-child(3) h3,#network .network-grid article:nth-child(3) p{max-width:48%!important}
  #network .network-grid article:nth-child(4){min-height:230px!important}
  #network .network-grid article:nth-child(4):before{right:0;top:19%;width:48%;height:62%}
  #network .network-grid article:nth-child(4):after{right:0;width:52%}
  #network .network-grid article:nth-child(4) h3,#network .network-grid article:nth-child(4) p{max-width:50%!important}
}
'''

text = text.replace('</style>', css + '\n</style>', 1)
path.write_text(text, encoding='utf-8')
