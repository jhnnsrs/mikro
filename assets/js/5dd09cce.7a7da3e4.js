"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[51],{3905:function(e,t,r){r.d(t,{Zo:function(){return u},kt:function(){return m}});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function l(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?l(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function o(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var s=n.createContext({}),p=function(e){var t=n.useContext(s),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},u=function(e){var t=p(e.components);return n.createElement(s.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,l=e.originalType,s=e.parentName,u=o(e,["components","mdxType","originalType","parentName"]),d=p(r),m=a,k=d["".concat(s,".").concat(m)]||d[m]||c[m]||l;return r?n.createElement(k,i(i({ref:t},u),{},{components:r})):n.createElement(k,i({ref:t},u))}));function m(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var l=r.length,i=new Array(l);i[0]=d;var o={};for(var s in t)hasOwnProperty.call(t,s)&&(o[s]=t[s]);o.originalType=e,o.mdxType="string"==typeof e?e:a,i[1]=o;for(var p=2;p<l;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}d.displayName="MDXCreateElement"},2468:function(e,t,r){r.r(t),r.d(t,{assets:function(){return u},contentTitle:function(){return s},default:function(){return m},frontMatter:function(){return o},metadata:function(){return p},toc:function(){return c}});var n=r(7462),a=r(3366),l=(r(7294),r(3905)),i=["components"],o={sidebar_label:"traits",title:"traits"},s=void 0,p={unversionedId:"reference/traits",id:"reference/traits",title:"traits",description:"Traits for Mikro.",source:"@site/docs/reference/traits.md",sourceDirName:"reference",slug:"/reference/traits",permalink:"/mikro/docs/reference/traits",editUrl:"https://github.com/jhnnsrs/mikro/edit/master/website/docs/reference/traits.md",tags:[],version:"current",frontMatter:{sidebar_label:"traits",title:"traits"},sidebar:"tutorialSidebar",previous:{title:"structures",permalink:"/mikro/docs/reference/structures"},next:{title:"widgets",permalink:"/mikro/docs/reference/widgets"}},u={},c=[{value:"Representation Objects",id:"representation-objects",level:2},{value:"data",id:"data",level:4},{value:"ROI Objects",id:"roi-objects",level:2},{value:"get_identifier",id:"get_identifier",level:4},{value:"ashrink",id:"ashrink",level:4},{value:"vector_data",id:"vector_data",level:4},{value:"Table Objects",id:"table-objects",level:2},{value:"data",id:"data-1",level:4},{value:"Vectorizable Objects",id:"vectorizable-objects",level:2},{value:"list_from_numpyarray",id:"list_from_numpyarray",level:4}],d={toc:c};function m(e){var t=e.components,r=(0,a.Z)(e,i);return(0,l.kt)("wrapper",(0,n.Z)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("p",null,"Traits for Mikro."),(0,l.kt)("p",null,"Traits are mixins that are added to every graphql type that exists on the mikro schema.\nWe use them to add functionality to the graphql types that extend from the base type."),(0,l.kt)("p",null,"Every GraphQL Model on Mikro gets a identifier and shrinking methods to ensure the compatibliity\nwith arkitekt. This is done by adding the identifier and the shrinking methods to the graphql type.\nIf you want to add your own traits to the graphql type, you can do so by adding them in the graphql\n.config.yaml file."),(0,l.kt)("h2",{id:"representation-objects"},"Representation Objects"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class Representation(BaseModel, ShrinkByID)\n")),(0,l.kt)("p",null,"Representation Trait"),(0,l.kt)("p",null,"Implements both identifier and shrinking methods.\nAlso Implements the data attribute"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"data")," ",(0,l.kt)("em",{parentName:"li"},"xarray.Dataset")," - The data of the representation.")),(0,l.kt)("h4",{id:"data"},"data"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef data() -> xr.DataArray\n")),(0,l.kt)("p",null,"The Data of the Representation as an xr.DataArray"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Returns"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"xr.DataArray")," - The associated object.")),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Raises"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"AssertionError")," - If the representation has no store attribute quries")),(0,l.kt)("h2",{id:"roi-objects"},"ROI Objects"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class ROI(BaseModel, ShrinkByID)\n")),(0,l.kt)("p",null,"Additional Methods for ROI"),(0,l.kt)("h4",{id:"get_identifier"},"get","_","identifier"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@classmethod\ndef get_identifier(cls)\n")),(0,l.kt)("p",null,"THis classes identifier on the platform"),(0,l.kt)("h4",{id:"ashrink"},"ashrink"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"async def ashrink()\n")),(0,l.kt)("p",null,"Shrinks this to a unique identifier on\nthe mikro server"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Returns"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"str")," - The unique identifier")),(0,l.kt)("h4",{id:"vector_data"},"vector","_","data"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef vector_data() -> np.ndarray\n")),(0,l.kt)("p",null,"A numpy array of the vectors of the ROI"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Returns"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"np.ndarray")," - ",(0,l.kt)("em",{parentName:"li"},"description"))),(0,l.kt)("h2",{id:"table-objects"},"Table Objects"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class Table(BaseModel, ShrinkByID)\n")),(0,l.kt)("p",null,"Table Trait"),(0,l.kt)("p",null,"Implements both identifier and shrinking methods.\nAlso Implements the data attribute"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"data")," ",(0,l.kt)("em",{parentName:"li"},"pd.DataFrame")," - The data of the table.")),(0,l.kt)("h4",{id:"data-1"},"data"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef data() -> pd.DataFrame\n")),(0,l.kt)("p",null,"The data of this table as a pandas dataframe"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Returns"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"pd.DataFrame")," - The Dataframe")),(0,l.kt)("h2",{id:"vectorizable-objects"},"Vectorizable Objects"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class Vectorizable()\n")),(0,l.kt)("h4",{id:"list_from_numpyarray"},"list","_","from","_","numpyarray"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"@classmethod\ndef list_from_numpyarray(cls: T, x: np.ndarray) -> List[T]\n")),(0,l.kt)("p",null,"Creates a list of InputVector from a numpya array"),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"vector_list")," ",(0,l.kt)("em",{parentName:"li"},"List[List","[float]","]")," - A list of lists of floats")),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"Returns"),":"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"List[Vectorizable]")," - A list of InputVector")))}m.isMDXComponent=!0}}]);