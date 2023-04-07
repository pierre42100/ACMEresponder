"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[581],{4137:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>f});var n=r(7294);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var l=n.createContext({}),c=function(e){var t=n.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},p=function(e){var t=c(e.components);return n.createElement(l.Provider,{value:t},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,a=e.originalType,l=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),u=c(r),m=o,f=u["".concat(l,".").concat(m)]||u[m]||d[m]||a;return r?n.createElement(f,i(i({ref:t},p),{},{components:r})):n.createElement(f,i({ref:t},p))}));function f(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=r.length,i=new Array(a);i[0]=m;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:o,i[1]=s;for(var c=2;c<a;c++)i[c]=r[c];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}m.displayName="MDXCreateElement"},9844:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>d,frontMatter:()=>a,metadata:()=>s,toc:()=>c});var n=r(7462),o=(r(7294),r(4137));const a={sidebar_position:2},i="Setup for production",s={unversionedId:"setup",id:"setup",title:"Setup for production",description:"Prepare the environment",source:"@site/docs/setup.md",sourceDirName:".",slug:"/setup",permalink:"/docs/setup",draft:!1,editUrl:"https://github.com/pierre42100/ACMEresponder/tree/master/docs/docs/setup.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"Discover ACMEResponder",permalink:"/docs/intro"},next:{title:"Configuration",permalink:"/docs/config"}},l={},c=[{value:"Prepare the environment",id:"prepare-the-environment",level:2},{value:"Prepare the storage",id:"prepare-the-storage",level:2},{value:"Prepare the certification authority",id:"prepare-the-certification-authority",level:2},{value:"Using Docker",id:"using-docker",level:2},{value:"Install it from sources",id:"install-it-from-sources",level:2},{value:"Configuration",id:"configuration",level:2},{value:"Build Docker image",id:"build-docker-image",level:2}],p={toc:c},u="wrapper";function d(e){let{components:t,...r}=e;return(0,o.kt)(u,(0,n.Z)({},p,r,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"setup-for-production"},"Setup for production"),(0,o.kt)("h2",{id:"prepare-the-environment"},"Prepare the environment"),(0,o.kt)("p",null,"In order to run an ACME responder, you will need:"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},"A Linux appliance with the 443 open"),(0,o.kt)("li",{parentName:"ul"},"Access to the port 80 of the clients"),(0,o.kt)("li",{parentName:"ul"},"A reverse proxy with a valid TLS certificate")),(0,o.kt)("h2",{id:"prepare-the-storage"},"Prepare the storage"),(0,o.kt)("p",null,"In order to use ACMEResponder, you must first create a directory to store the CA certificate and the accounts public keys:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"mkdir storage\n")),(0,o.kt)("h2",{id:"prepare-the-certification-authority"},"Prepare the certification authority"),(0,o.kt)("p",null,"You also (obviously) need a certification authority to sign the issued certificates. It is up to you to obtain a valid Certificate Authority."),(0,o.kt)("p",null,"However, for testing purpose, you can also create a self-signed certificate :"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},'# Create a CA private key\nopenssl genrsa -out storage/ca-privkey.pem 4096\n\n# Create a CA signing key\nopenssl req -new -key storage/ca-privkey.pem -x509 -days 1000 -out storage/ca-pubkey.pem -subj "/C=FR/ST=Loire/L=StEtienne/O=Global Security/OU=IT Department/CN=example.com"\n')),(0,o.kt)("admonition",{type:"danger"},(0,o.kt)("p",{parentName:"admonition"},"Without a certificate issued by a well-known root certification authority and authorized to sign certificate (",(0,o.kt)("inlineCode",{parentName:"p"},"IsCA")," constraint set to true), the certificates issued by ACMEResponder won't be recognized by default by the TLS endpoints software programs (browsers, CLI utilities...)"),(0,o.kt)("p",{parentName:"admonition"},"However, you can still use your self-signed certification authority on your own devices by installing them on your trusted certificates store.")),(0,o.kt)("h2",{id:"using-docker"},"Using Docker"),(0,o.kt)("p",null,"The easiest way to install ACMEResponder is to use our Docker image. You can run it using the following command:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"docker run --rm -v $(pwd)/storage:/storage -p 80:80 pierre42100/acme-responder\n")),(0,o.kt)("h2",{id:"install-it-from-sources"},"Install it from sources"),(0,o.kt)("p",null,"You can also install ACMEResponder from source. In order to do so:"),(0,o.kt)("ol",null,(0,o.kt)("li",{parentName:"ol"},"You must first clone the source code of the repository:")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"git clone https://github.com/pierre42100/ACMEresponder\ncd ACMEresponder\n")),(0,o.kt)("ol",{start:3},(0,o.kt)("li",{parentName:"ol"},"Create a Python environment:")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"python3 -m venv venv\n")),(0,o.kt)("ol",{start:3},(0,o.kt)("li",{parentName:"ol"},"Switch the shell to the created environment:")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"source venv/bin/activate\n")),(0,o.kt)("ol",{start:4},(0,o.kt)("li",{parentName:"ol"},"Setup dependencies")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"pip install -r requirements.txt\n")),(0,o.kt)("ol",{start:5},(0,o.kt)("li",{parentName:"ol"},"You should then be ready to run the server:")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"STORAGE_PATH=/path/to/storage uvicorn src.server:app --host 0.0.0.0 --port 80\n")),(0,o.kt)("h2",{id:"configuration"},"Configuration"),(0,o.kt)("p",null,"Some aspects of ACMEResponder can be customized. See the ",(0,o.kt)("a",{parentName:"p",href:"./config"},"Configuration")," section to learn more."),(0,o.kt)("h2",{id:"build-docker-image"},"Build Docker image"),(0,o.kt)("p",null,"If you wish to build by yourself the Docker image of the project, you can do so by running the following command:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"bash build-docker-image.sh\n")))}d.isMDXComponent=!0}}]);