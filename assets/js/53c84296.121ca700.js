"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[334],{4137:(e,t,n)=>{n.d(t,{Zo:()=>u,kt:()=>h});var r=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),c=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},u=function(e){var t=c(e.components);return r.createElement(s.Provider,{value:t},e.children)},p="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},m=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,s=e.parentName,u=l(e,["components","mdxType","originalType","parentName"]),p=c(n),m=o,h=p["".concat(s,".").concat(m)]||p[m]||d[m]||i;return n?r.createElement(h,a(a({ref:t},u),{},{components:n})):r.createElement(h,a({ref:t},u))}));function h(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=m;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[p]="string"==typeof e?e:o,a[1]=l;for(var c=2;c<i;c++)a[c]=n[c];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}m.displayName="MDXCreateElement"},7037:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>a,default:()=>d,frontMatter:()=>i,metadata:()=>l,toc:()=>c});var r=n(7462),o=(n(7294),n(4137));const i={sidebar_position:7},a="Evaluation",l={unversionedId:"evaluation",id:"evaluation",title:"Evaluation",description:'This project was achieved during a "Python for Security" course at EPITA.',source:"@site/docs/evaluation.md",sourceDirName:".",slug:"/evaluation",permalink:"/docs/evaluation",draft:!1,editUrl:"https://github.com/pierre42100/ACMEresponder/tree/master/docs/docs/evaluation.md",tags:[],version:"current",sidebarPosition:7,frontMatter:{sidebar_position:7},sidebar:"tutorialSidebar",previous:{title:"Technical choices",permalink:"/docs/tech_choices"}},s={},c=[{value:"Environment",id:"environment",level:2},{value:"Get the source code",id:"get-the-source-code",level:2},{value:"Prepare the storage",id:"prepare-the-storage",level:2},{value:"Execute the solution",id:"execute-the-solution",level:2},{value:"Test certificates issuance",id:"test-certificates-issuance",level:2},{value:"Building Docker image",id:"building-docker-image",level:2}],u={toc:c},p="wrapper";function d(e){let{components:t,...n}=e;return(0,o.kt)(p,(0,r.Z)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"evaluation"},"Evaluation"),(0,o.kt)("p",null,'This project was achieved during a "Python for Security" course at EPITA.'),(0,o.kt)("p",null,"In order to validate the course, the teacher asked us to give him some guidelines to allow him to easily and quickly try out the solution built. Here are presented those instructions."),(0,o.kt)("h2",{id:"environment"},"Environment"),(0,o.kt)("p",null,"In order to assess our ACME responder, we decided to use the most popular ACME client, ",(0,o.kt)("inlineCode",{parentName:"p"},"certbot"),". (",(0,o.kt)("a",{parentName:"p",href:"https://certbot.eff.org/"},"official website"),")."),(0,o.kt)("p",null,"Unfortunately, Certbot is certainly the most rigorous ACME client, as the contrary of sewer (used in unit testing, which is more permissive). Certbot expect from the ACME provider a strict compliance to the standards. One of these requirements is that an ACME server shall not be queried in HTTP. "),(0,o.kt)("p",null,"Therefore, we had to set up a local environment where ACME responder could be reached in HTTPS. In order to achieve this goal, we needed to create a self-signed authority that would sign a certificate used for a TLS reverse proxy."),(0,o.kt)("p",null,"We built such environment using Docker Compose :"),(0,o.kt)("mermaid",{value:"flowchart TD\n    srv[ACME Responder<br><small>Our solution</small>]\n    proxy[Secure<br><small>Reverse Proxy / TLS endpoint</small>]\n    client[Client<br><small>Hostname: client</small>]\n\n    \n    proxy--\x3e|Orders<br><small><i>http:80</i></small>|srv\n    client--\x3e|Orders<br><small><i>https:443</i></small>|proxy\n    srv-.->|Query challenge<br><small><i>http:80</i></small>|client\n\n    classDef blue fill:blue,stroke:#333,stroke-width:4px;\n    class srv blue"}),(0,o.kt)("p",null,"In this environment, the client (hostname ",(0,o.kt)("inlineCode",{parentName:"p"},"client"),") can query the ACMEResponder on the URL https://secure/ (hostname ",(0,o.kt)("inlineCode",{parentName:"p"},"server"),"), which is a reverse proxy that includes a TLS endpoint."),(0,o.kt)("admonition",{type:"info"},(0,o.kt)("p",{parentName:"admonition"},"The certificate of the reverse proxy is signed by a self-signed Certification Authority, so the client must either accept all certificates or add the self-signed Certification Authority to its trusted certificates store. We opted for the latter solution.")),(0,o.kt)("p",null,"The reverse proxy redirect traffic to the ",(0,o.kt)("inlineCode",{parentName:"p"},"acme")," container, which runs our solution. This machine can directly query the client for the authentication challenges during certificates issuance."),(0,o.kt)("h2",{id:"get-the-source-code"},"Get the source code"),(0,o.kt)("p",null,"In order to get started, you must first clone the repository:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"git clone https://github.com/pierre42100/ACMEresponder\n")),(0,o.kt)("p",null,"Then you must enter inside the ",(0,o.kt)("inlineCode",{parentName:"p"},"evaluation")," directory:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"cd ACMEresponder/evaluation\n")),(0,o.kt)("h2",{id:"prepare-the-storage"},"Prepare the storage"),(0,o.kt)("p",null,"First, you need to initialize the Certification Authority that will be used to sign issued certificates :"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},'# Create storage directory\nmkdir storage\n\n# Create a CA private key\nopenssl genrsa -out storage/ca-privkey.pem 4096\n\n# Create a CA signing key\nopenssl req -new -key storage/ca-privkey.pem -x509 -days 1000 -out storage/ca-pubkey.pem -subj "/C=FR/ST=Loire/L=StEtienne/O=Global Security/OU=IT Department/CN=example.com"\n')),(0,o.kt)("h2",{id:"execute-the-solution"},"Execute the solution"),(0,o.kt)("p",null,"In order to run the solution, you must have ",(0,o.kt)("inlineCode",{parentName:"p"},"docker")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"docker-compose")," installed on your computer."),(0,o.kt)("p",null,"Deploy the ",(0,o.kt)("inlineCode",{parentName:"p"},"docker-compose")," network (still from the ",(0,o.kt)("inlineCode",{parentName:"p"},"evaluation")," directory):"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"docker-compose up\n")),(0,o.kt)("p",null,"Three Docker images will be pulled from the Docker Hub, including our solution, in production mode."),(0,o.kt)("h2",{id:"test-certificates-issuance"},"Test certificates issuance"),(0,o.kt)("p",null,"In order to test certificates issuance, open a new shell (leave the window with ",(0,o.kt)("inlineCode",{parentName:"p"},"docker-compose")," open) and open a new shell on the ",(0,o.kt)("inlineCode",{parentName:"p"},"client")," container:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"docker exec -it evaluation-client-1 /bin/bash\n")),(0,o.kt)("admonition",{type:"info"},(0,o.kt)("p",{parentName:"admonition"},"If the previous command does not work, use the command ",(0,o.kt)("inlineCode",{parentName:"p"},"docker ps")," to get the name of the container running our client (",(0,o.kt)("inlineCode",{parentName:"p"},"pierre42100/acme-eval-client"),"):"),(0,o.kt)("pre",{parentName:"admonition"},(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"docker ps | grep pierre42100/acme-eval-client\n"))),(0,o.kt)("p",null,"In the container, you can request a new certificate issuance:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"REQUESTS_CA_BUNDLE=/myca.crt certbot certonly -n  --webroot -w /storage -d client --server https://secure/directory --agree-tos --email mymail@corp.com\n")),(0,o.kt)("p",null,"If everything goes well, you should get an output similar to that one:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre"},"Saving debug log to /var/log/letsencrypt/letsencrypt.log\nAccount registered.\nRequesting a certificate for client\n\nSuccessfully received certificate.\nCertificate is saved at: /etc/letsencrypt/live/client/fullchain.pem\nKey is saved at:         /etc/letsencrypt/live/client/privkey.pem\nThis certificate expires on 2023-05-07.\nThese files will be updated when the certificate renews.\n\nNEXT STEPS:\n- The certificate will need to be renewed before it expires. Certbot can automatically renew the certificate in the background, but you may need to take steps to enable that functionality. See https://certbot.org/renewal-setup for instructions.\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIf you like Certbot, please consider supporting our work by:\n * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate\n * Donating to EFF:                    https://eff.org/donate-le\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")),(0,o.kt)("p",null,"You can then inspect the details of the generated certificate:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"openssl x509 -in /etc/letsencrypt/live/client/fullchain.pem -text -noout\n")),(0,o.kt)("admonition",{type:"note"},(0,o.kt)("p",{parentName:"admonition"},"In our case, the common name will be ",(0,o.kt)("inlineCode",{parentName:"p"},"client")," (the name of the container in the ",(0,o.kt)("inlineCode",{parentName:"p"},"docker-compose")," network)")),(0,o.kt)("admonition",{type:"info"},(0,o.kt)("p",{parentName:"admonition"},"And that's it! You just generated a certificate from your very own ACME provider!!!")),(0,o.kt)("h2",{id:"building-docker-image"},"Building Docker image"),(0,o.kt)("p",null,"By default, the given directions will pull the images from the Docker hub. However, you can also build by yourself the Docker images used in this demonstration :"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"cd /root/of/repo\n\n# Build main image (ACME Responder)\nbash build-docker-image.sh\n\n# Build reverse proxy image\ncd evaluation/reverse-proxy\nbash build-docker-image.sh\n\n# Build client image\ncd evaluation/test-client\nbash build-docker-image.sh\n")))}d.isMDXComponent=!0}}]);