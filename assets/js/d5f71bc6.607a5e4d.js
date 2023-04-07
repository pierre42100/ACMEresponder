"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[367],{4137:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>d});var a=r(7294);function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,a)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function l(e,t){if(null==e)return{};var r,a,n=function(e,t){if(null==e)return{};var r,a,n={},o=Object.keys(e);for(a=0;a<o.length;a++)r=o[a],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)r=o[a],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}var c=a.createContext({}),s=function(e){var t=a.useContext(c),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},p=function(e){var t=s(e.components);return a.createElement(c.Provider,{value:t},e.children)},u="mdxType",h={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},m=a.forwardRef((function(e,t){var r=e.components,n=e.mdxType,o=e.originalType,c=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),u=s(r),m=n,d=u["".concat(c,".").concat(m)]||u[m]||h[m]||o;return r?a.createElement(d,i(i({ref:t},p),{},{components:r})):a.createElement(d,i({ref:t},p))}));function d(e,t){var r=arguments,n=t&&t.mdxType;if("string"==typeof e||n){var o=r.length,i=new Array(o);i[0]=m;var l={};for(var c in t)hasOwnProperty.call(t,c)&&(l[c]=t[c]);l.originalType=e,l[u]="string"==typeof e?e:n,i[1]=l;for(var s=2;s<o;s++)i[s]=r[s];return a.createElement.apply(null,i)}return a.createElement.apply(null,r)}m.displayName="MDXCreateElement"},674:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>c,contentTitle:()=>i,default:()=>h,frontMatter:()=>o,metadata:()=>l,toc:()=>s});var a=r(7462),n=(r(7294),r(4137));const o={sidebar_position:6},i="Technical choices",l={unversionedId:"tech_choices",id:"tech_choices",title:"Technical choices",description:"The programming language: Python",source:"@site/docs/tech_choices.md",sourceDirName:".",slug:"/tech_choices",permalink:"/docs/tech_choices",draft:!1,editUrl:"https://github.com/pierre42100/ACMEresponder/tree/master/docs/docs/tech_choices.md",tags:[],version:"current",sidebarPosition:6,frontMatter:{sidebar_position:6},sidebar:"tutorialSidebar",previous:{title:"Certificate issuance diagram",permalink:"/docs/diagram"},next:{title:"Evaluation",permalink:"/docs/evaluation"}},c={},s=[{value:"The programming language: Python",id:"the-programming-language-python",level:2},{value:"The API framework: FastAPI",id:"the-api-framework-fastapi",level:2},{value:"The ACME protocol test library: sewer",id:"the-acme-protocol-test-library-sewer",level:2},{value:"Included features",id:"included-features",level:2},{value:"The project itself: an ACME implementation",id:"the-project-itself-an-acme-implementation",level:2}],p={toc:s},u="wrapper";function h(e){let{components:t,...r}=e;return(0,n.kt)(u,(0,a.Z)({},p,r,{components:t,mdxType:"MDXLayout"}),(0,n.kt)("h1",{id:"technical-choices"},"Technical choices"),(0,n.kt)("h2",{id:"the-programming-language-python"},"The programming language: Python"),(0,n.kt)("p",null,"This project was built using the Python programming language."),(0,n.kt)("p",null,'This language was not really chosen. Indeed, it has imposed by the context this project was lead, during an EPITA "Python for security" course.'),(0,n.kt)("p",null,"However, the simplicity of this programming language made it rather easy to build a working prototype."),(0,n.kt)("h2",{id:"the-api-framework-fastapi"},"The API framework: FastAPI"),(0,n.kt)("p",null,"FastAPI is a well-known REST framework. Because, at the time of the construction  of this project, it had more than 56k stars and 4.7k forks ",(0,n.kt)("a",{parentName:"p",href:"https://github.com/tiangolo/fastapi"},"on GitHub"),", we can make the following assertions about this tool:"),(0,n.kt)("ul",null,(0,n.kt)("li",{parentName:"ul"},"It is worth it to spend time using it, otherwise it wouldn't be so popular"),(0,n.kt)("li",{parentName:"ul"},"Security researchers have certainly helped to harden the security of its source code.")),(0,n.kt)("p",null,"Moreover, ",(0,n.kt)("a",{parentName:"p",href:"https://fastapi.tiangolo.com/"},"the documentation of FastAPI")," is well furbished, making it easy to get started with it."),(0,n.kt)("h2",{id:"the-acme-protocol-test-library-sewer"},"The ACME protocol test library: sewer"),(0,n.kt)("p",null,"In order to build our units tests, we needed a ACME-capable library that would act as a client to the ACME protocol. The requirements for such library were the following:"),(0,n.kt)("ul",null,(0,n.kt)("li",{parentName:"ul"},"The library must be able to act as an ACME client, following the RFC 8555 standard"),(0,n.kt)("li",{parentName:"ul"},"It must offer an API that allow programmatic calls, with some aspects hook-able:",(0,n.kt)("ul",{parentName:"li"},(0,n.kt)("li",{parentName:"ul"},"The library must allow to perform clear-text exchanges with the ACME backend"),(0,n.kt)("li",{parentName:"ul"},"The library must be hook-able, allowing custom code to handle challenge deployment"))),(0,n.kt)("li",{parentName:"ul"},"It must be written in Python"),(0,n.kt)("li",{parentName:"ul"},"The library must be usable with a free license")),(0,n.kt)("p",null,"The ",(0,n.kt)("a",{parentName:"p",href:"https://github.com/komuw/sewer"},"Sewer")," library addresses all these requirements."),(0,n.kt)("h2",{id:"included-features"},"Included features"),(0,n.kt)("ul",null,(0,n.kt)("li",{parentName:"ul"},"\u2705 ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-7.1.1"},"Directory listing"),". This is the entry-point to all the others features of the protocol. Without it, ACME is not ACME."),(0,n.kt)("li",{parentName:"ul"},"\u2705 ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-7.3"},"Account creation"),". Accounts are required to manage orders."),(0,n.kt)("li",{parentName:"ul"},"\u2705 ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-7.4"},"Orders creation and management"),": Orders are the basis of certificates generation and retrieval"),(0,n.kt)("li",{parentName:"ul"},"\u2705 ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-8.3"},"HTTP-based challenge")," HTTP Challenges are the more common and more secure way to authenticate servers through ACME"),(0,n.kt)("li",{parentName:"ul"},"\u274c ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-8.4"},"DNS-based challenges")," DNS based-challenge are quite challenging to test in an automated way. Due to constrained time, we decided not to implement it."),(0,n.kt)("li",{parentName:"ul"},"\u274c ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-7.6"},"Certificates revocation"),". We made explicitly the choice not to implement certificates revocations because :",(0,n.kt)("ul",{parentName:"li"},(0,n.kt)("li",{parentName:"ul"},"It would add significant overhead in the management of the orders (the orders would have to be persisted)"),(0,n.kt)("li",{parentName:"ul"},"It is often preferable, especially in controlled environment, to reduce the lifetime of the certificates rather than revoking leaked certificates."))),(0,n.kt)("li",{parentName:"ul"},"\u274c ",(0,n.kt)("a",{parentName:"li",href:"https://www.rfc-editor.org/rfc/rfc8555#section-7.3.5"},"Account key rollover and deactivation"),". This feature present an interest only if the revocation itself is implemented, to prevent from unwanted revocation in case of account private key revocation. Because we did not implement revocation, it was not necessary to handle accounts key revocation. ")),(0,n.kt)("h2",{id:"the-project-itself-an-acme-implementation"},"The project itself: an ACME implementation"),(0,n.kt)("p",null,"Let's Encrypt is a fantastic technology that we have been using for years to issue new certificates."),(0,n.kt)("p",null,"We saw this project as an opportunity to discover how Let's Encrypt does its magic."))}h.isMDXComponent=!0}}]);