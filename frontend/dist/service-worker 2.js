if(!self.define){let e,n={};const s=(s,i)=>(s=new URL(s+".js",i).href,n[s]||new Promise((n=>{if("document"in self){const e=document.createElement("script");e.src=s,e.onload=n,document.head.appendChild(e)}else e=s,importScripts(s),n()})).then((()=>{let e=n[s];if(!e)throw new Error(`Module ${s} didn’t register its module`);return e})));self.define=(i,o)=>{const r=e||("document"in self?document.currentScript.src:"")||location.href;if(n[r])return;let l={};const t=e=>s(e,r),f={module:{uri:r},exports:l,require:t};n[r]=Promise.all(i.map((e=>f[e]||t(e)))).then((e=>(o(...e),l)))}}define(["./workbox-5b385ed2"],(function(e){"use strict";e.setCacheNameDetails({prefix:"finale-project"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/additionalComments.md",revision:"a28080e240a62b00bdf5e8e3d3bfac72"},{url:"/css/app.b9c42d32.css",revision:null},{url:"/css/chunk-vendors.1b6ec2d0.css",revision:null},{url:"/fonts/materialdesignicons-webfont.21f691f0.ttf",revision:null},{url:"/fonts/materialdesignicons-webfont.54b0f60d.woff2",revision:null},{url:"/fonts/materialdesignicons-webfont.5d875350.eot",revision:null},{url:"/fonts/materialdesignicons-webfont.d671cbf6.woff",revision:null},{url:"/index.html",revision:"c224be129b4e47044cf10917663a41b4"},{url:"/js/app.13825a4d.js",revision:null},{url:"/js/chunk-vendors.843595c6.js",revision:null},{url:"/js/webfontloader.02550f3f.js",revision:null},{url:"/manifest.json",revision:"a0325f7fc3b1855af67701dc7ddbd210"},{url:"/passive-event-notoriousBug.js",revision:"fd7f5f524c963b9491f3a4d2f70f32d0"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"},{url:"/to-do.md",revision:"07fb49f0d0c4f8035042597e8de701f1"}],{})}));
//# sourceMappingURL=service-worker.js.map