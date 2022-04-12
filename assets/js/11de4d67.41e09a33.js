"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[235],{3905:function(e,t,r){r.d(t,{Zo:function(){return s},kt:function(){return m}});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function l(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var p=n.createContext({}),u=function(e){var t=n.useContext(p),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},s=function(e){var t=u(e.components);return n.createElement(p.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,p=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),d=u(r),m=a,f=d["".concat(p,".").concat(m)]||d[m]||c[m]||o;return r?n.createElement(f,i(i({ref:t},s),{},{components:r})):n.createElement(f,i({ref:t},s))}));function m(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=d;var l={};for(var p in t)hasOwnProperty.call(t,p)&&(l[p]=t[p]);l.originalType=e,l.mdxType="string"==typeof e?e:a,i[1]=l;for(var u=2;u<o;u++)i[u]=r[u];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}d.displayName="MDXCreateElement"},8945:function(e,t,r){r.r(t),r.d(t,{assets:function(){return s},contentTitle:function(){return p},default:function(){return m},frontMatter:function(){return l},metadata:function(){return u},toc:function(){return c}});var n=r(7462),a=r(3366),o=(r(7294),r(3905)),i=["components"],l={sidebar_label:"parquet",title:"links.parquet"},p=void 0,u={unversionedId:"reference/links/parquet",id:"reference/links/parquet",title:"links.parquet",description:"DataLayerParquetUploadLink Objects",source:"@site/docs/reference/links/parquet.md",sourceDirName:"reference/links",slug:"/reference/links/parquet",permalink:"/mikro/docs/reference/links/parquet",editUrl:"https://github.com/jhnnsrs/mikro/edit/master/website/docs/reference/links/parquet.md",tags:[],version:"current",frontMatter:{sidebar_label:"parquet",title:"links.parquet"},sidebar:"tutorialSidebar",previous:{title:"funcs",permalink:"/mikro/docs/reference/funcs"},next:{title:"xarray",permalink:"/mikro/docs/reference/links/xarray"}},s={},c=[{value:"DataLayerParquetUploadLink Objects",id:"datalayerparquetuploadlink-objects",level:2},{value:"store_df",id:"store_df",level:4},{value:"aparse",id:"aparse",level:4},{value:"__aenter__",id:"__aenter__",level:4}],d={toc:c};function m(e){var t=e.components,r=(0,a.Z)(e,i);return(0,o.kt)("wrapper",(0,n.Z)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h2",{id:"datalayerparquetuploadlink-objects"},"DataLayerParquetUploadLink Objects"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"class DataLayerParquetUploadLink(ParsingLink)\n")),(0,o.kt)("p",null,"Data Layer Parquet Upload Link"),(0,o.kt)("p",null,"This link is used to upload a DataFrame to a DataLayer.\nIt parses queries, mutatoin and subscription arguments and\nuploads the items to the DataLayer, and substitures the\nDataFrame with the S3 path."),(0,o.kt)("p",null,(0,o.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("inlineCode",{parentName:"li"},"ParsingLink")," ",(0,o.kt)("strong",{parentName:"li"},"type")," - ",(0,o.kt)("em",{parentName:"li"},"description"))),(0,o.kt)("h4",{id:"store_df"},"store","_","df"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"def store_df(df: pd.DataFrame) -> None\n")),(0,o.kt)("p",null,"Store a DataFrame in the DataLayer"),(0,o.kt)("h4",{id:"aparse"},"aparse"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"async def aparse(operation: Operation) -> Operation\n")),(0,o.kt)("p",null,"Parse the operation (Async)"),(0,o.kt)("p",null,"Extracts the DataFrame from the operation and uploads it to the DataLayer."),(0,o.kt)("p",null,(0,o.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("inlineCode",{parentName:"li"},"operation")," ",(0,o.kt)("em",{parentName:"li"},"Operation")," - The operation to parse")),(0,o.kt)("p",null,(0,o.kt)("strong",{parentName:"p"},"Returns"),":"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("inlineCode",{parentName:"li"},"Operation")," - ",(0,o.kt)("em",{parentName:"li"},"description"))),(0,o.kt)("h4",{id:"__aenter__"},"_","_","aenter","_","_"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"async def __aenter__() -> None\n")),(0,o.kt)("p",null,"Enter the executor"))}m.isMDXComponent=!0}}]);