/*
 (function(m){m.color={};m.color.make=function(u,p,g,h){var k={};k.r=u||0;k.g=p||0;k.b=g||0;k.a=null!=h?h:1;k.add=function(g,m){for(var h=0;h<g.length;++h)k[g.charAt(h)]+=m;return k.normalize()};k.scale=function(g,m){for(var h=0;h<g.length;++h)k[g.charAt(h)]*=m;return k.normalize()};k.toString=function(){return 1<=k.a?"rgb("+[k.r,k.g,k.b].join()+")":"rgba("+[k.r,k.g,k.b,k.a].join()+")"};k.normalize=function(){function g(k,m,h){return m<k?k:m>h?h:m}k.r=g(0,parseInt(k.r),255);k.g=g(0,parseInt(k.g),255);
 k.b=g(0,parseInt(k.b),255);k.a=g(0,k.a,1);return k};k.clone=function(){return m.color.make(k.r,k.b,k.g,k.a)};return k.normalize()};m.color.extract=function(u,p){var g;do{g=u.css(p).toLowerCase();if(""!=g&&"transparent"!=g)break;u=u.parent()}while(u.length&&!m.nodeName(u.get(0),"body"));"rgba(0, 0, 0, 0)"==g&&(g="transparent");return m.color.parse(g)};m.color.parse=function(u){var p,g=m.color.make;if(p=/rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(u))return g(parseInt(p[1],
 10),parseInt(p[2],10),parseInt(p[3],10));if(p=/rgba\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(u))return g(parseInt(p[1],10),parseInt(p[2],10),parseInt(p[3],10),parseFloat(p[4]));if(p=/rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(u))return g(2.55*parseFloat(p[1]),2.55*parseFloat(p[2]),2.55*parseFloat(p[3]));if(p=/rgba\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(u))return g(2.55*
 parseFloat(p[1]),2.55*parseFloat(p[2]),2.55*parseFloat(p[3]),parseFloat(p[4]));if(p=/#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(u))return g(parseInt(p[1],16),parseInt(p[2],16),parseInt(p[3],16));if(p=/#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(u))return g(parseInt(p[1]+p[1],16),parseInt(p[2]+p[2],16),parseInt(p[3]+p[3],16));u=m.trim(u).toLowerCase();if("transparent"==u)return g(255,255,255,0);p=C[u]||[0,0,0];return g(p[0],p[1],p[2])};var C={aqua:[0,255,255],azure:[240,255,255],beige:[245,
 245,220],black:[0,0,0],blue:[0,0,255],brown:[165,42,42],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgrey:[169,169,169],darkgreen:[0,100,0],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkviolet:[148,0,211],fuchsia:[255,0,255],gold:[255,215,0],green:[0,128,0],indigo:[75,0,130],khaki:[240,230,140],lightblue:[173,216,230],lightcyan:[224,255,255],lightgreen:[144,238,
 144],lightgrey:[211,211,211],lightpink:[255,182,193],lightyellow:[255,255,224],lime:[0,255,0],magenta:[255,0,255],maroon:[128,0,0],navy:[0,0,128],olive:[128,128,0],orange:[255,165,0],pink:[255,192,203],purple:[128,0,128],violet:[128,0,128],red:[255,0,0],silver:[192,192,192],white:[255,255,255],yellow:[255,255,0]}})(jQuery);
 (function(m){function C(g,h){var k=h.children("."+g)[0];if(null==k&&(k=document.createElement("canvas"),k.className=g,m(k).css({direction:"ltr",position:"absolute",left:0,top:0}).appendTo(h),!k.getContext))if(window.G_vmlCanvasManager)k=window.G_vmlCanvasManager.initElement(k);else throw Error("Canvas is not available. If you're using IE with a fall-back such as Excanvas, then there's either a mistake in your conditional include, or the page has no DOCTYPE and is rendering in Quirks Mode.");this.element=
 k;k=this.context=k.getContext("2d");this.pixelRatio=(window.devicePixelRatio||1)/(k.webkitBackingStorePixelRatio||k.mozBackingStorePixelRatio||k.msBackingStorePixelRatio||k.oBackingStorePixelRatio||k.backingStorePixelRatio||1);this.resize(h.width(),h.height());this.textContainer=null;this.text={};this._textCache={}}function u(g,h,k,p){function s(a,c){c=[x].concat(c);for(var b=0;b<a.length;++b)a[b].apply(this,c)}function K(a){for(var c=[],b=0;b<a.length;++b){var d=m.extend(!0,{},e.series);null!=a[b].data?
 (d.data=a[b].data,delete a[b].data,m.extend(!0,d,a[b]),a[b].data=d.data):d.data=a[b];c.push(d)}w=c;b=w.length;c=-1;for(a=0;a<w.length;++a)d=w[a].color,null!=d&&(b--,"number"==typeof d&&d>c&&(c=d));b<=c&&(b=c+1);var c=[],f=e.colors,q=f.length,t=0;for(a=0;a<b;a++)d=m.color.parse(f[a%q]||"#666"),0==a%q&&a&&(t=0<=t?.5>t?-t-.2:0:-t),c[a]=d.scale("rgb",1+t);for(a=b=0;a<w.length;++a){d=w[a];null==d.color?(d.color=c[b].toString(),++b):"number"==typeof d.color&&(d.color=c[d.color].toString());if(null==d.lines.show){var y,
 f=!0;for(y in d)if(d[y]&&d[y].show){f=!1;break}f&&(d.lines.show=!0)}null==d.lines.zero&&(d.lines.zero=!!d.lines.fill);d.xaxis=L(E,u(d,"x"));d.yaxis=L(I,u(d,"y"))}ka()}function u(a,c){var b=a[c+"axis"];"object"==typeof b&&(b=b.n);"number"!=typeof b&&(b=1);return b}function F(){return m.grep(E.concat(I),function(a){return a})}function W(a){var c={},b,d;for(b=0;b<E.length;++b)(d=E[b])&&d.used&&(c["x"+d.n]=d.c2p(a.left));for(b=0;b<I.length;++b)(d=I[b])&&d.used&&(c["y"+d.n]=d.c2p(a.top));void 0!==c.x1&&
 (c.x=c.x1);void 0!==c.y1&&(c.y=c.y1);return c}function L(a,c){a[c-1]||(a[c-1]={n:c,direction:a==E?"x":"y",options:m.extend(!0,{},a==E?e.xaxis:e.yaxis)});return a[c-1]}function ka(){function a(a,b,c){b<a.datamin&&b!=-d&&(a.datamin=b);c>a.datamax&&c!=d&&(a.datamax=c)}var c=Number.POSITIVE_INFINITY,b=Number.NEGATIVE_INFINITY,d=Number.MAX_VALUE,f,q,t,y,r,e,l,g,k,n,h,D;m.each(F(),function(a,d){d.datamin=c;d.datamax=b;d.used=!1});for(f=0;f<w.length;++f)r=w[f],r.datapoints={points:[]},s(G.processRawData,
 [r,r.data,r.datapoints]);for(f=0;f<w.length;++f){r=w[f];h=r.data;D=r.datapoints.format;if(!D){D=[];D.push({x:!0,number:!0,required:!0});D.push({y:!0,number:!0,required:!0});if(r.bars.show||r.lines.show&&r.lines.fill)D.push({y:!0,number:!0,required:!1,defaultValue:0,autoscale:!!(r.bars.show&&r.bars.zero||r.lines.show&&r.lines.zero)}),r.bars.horizontal&&(delete D[D.length-1].y,D[D.length-1].x=!0);r.datapoints.format=D}if(null==r.datapoints.pointsize){r.datapoints.pointsize=D.length;l=r.datapoints.pointsize;
 e=r.datapoints.points;var v=r.lines.show&&r.lines.steps;r.xaxis.used=r.yaxis.used=!0;for(q=t=0;q<h.length;++q,t+=l){n=h[q];var T=null==n;if(!T)for(y=0;y<l;++y){g=n[y];if(k=D[y])k.number&&null!=g&&(g=+g,isNaN(g)?g=null:Infinity==g?g=d:-Infinity==g&&(g=-d)),null==g&&(k.required&&(T=!0),null!=k.defaultValue&&(g=k.defaultValue));e[t+y]=g}if(T)for(y=0;y<l;++y)g=e[t+y],null!=g&&(k=D[y],!1!==k.autoscale&&(k.x&&a(r.xaxis,g,g),k.y&&a(r.yaxis,g,g))),e[t+y]=null;else if(v&&0<t&&null!=e[t-l]&&e[t-l]!=e[t]&&e[t-
 l+1]!=e[t+1]){for(y=0;y<l;++y)e[t+l+y]=e[t+y];e[t+1]=e[t-l+1];t+=l}}}}for(f=0;f<w.length;++f)r=w[f],s(G.processDatapoints,[r,r.datapoints]);for(f=0;f<w.length;++f){r=w[f];e=r.datapoints.points;l=r.datapoints.pointsize;D=r.datapoints.format;n=t=c;v=h=b;for(q=0;q<e.length;q+=l)if(null!=e[q])for(y=0;y<l;++y)g=e[q+y],(k=D[y])&&!1!==k.autoscale&&g!=d&&g!=-d&&(k.x&&(g<t&&(t=g),g>h&&(h=g)),k.y&&(g<n&&(n=g),g>v&&(v=g)));if(r.bars.show){switch(r.bars.align){case "left":q=0;break;case "right":q=-r.bars.barWidth;
 break;default:q=-r.bars.barWidth/2}r.bars.horizontal?(n+=q,v+=q+r.bars.barWidth):(t+=q,h+=q+r.bars.barWidth)}a(r.xaxis,t,h);a(r.yaxis,n,v)}m.each(F(),function(a,d){d.datamin==c&&(d.datamin=null);d.datamax==b&&(d.datamax=null)})}function X(){R&&clearTimeout(R);M.unbind("mousemove",Y);M.unbind("mouseleave",Z);M.unbind("click",$);s(G.shutdown,[M])}function la(a){function c(a){return a}var b,d,f=a.options.transform||c,q=a.options.inverseTransform;"x"==a.direction?(b=a.scale=N/Math.abs(f(a.max)-f(a.min)),
 d=Math.min(f(a.max),f(a.min))):(b=a.scale=J/Math.abs(f(a.max)-f(a.min)),b=-b,d=Math.max(f(a.max),f(a.min)));a.p2c=f==c?function(a){return(a-d)*b}:function(a){return(f(a)-d)*b};a.c2p=q?function(a){return q(d+a/b)}:function(a){return d+a/b}}function ma(a){var c=a.labelWidth,b=a.labelHeight,d=a.options.position,f="x"===a.direction,q=a.options.tickLength,t=e.grid.axisMargin,y=e.grid.labelMargin,r=!0,g=!0,l=!0,k=!1;m.each(f?E:I,function(b,c){c&&(c.show||c.reserveSpace)&&(c===a?k=!0:c.options.position===
 d&&(k?g=!1:r=!1),k||(l=!1))});g&&(t=0);null==q&&(q=l?"full":5);isNaN(+q)||(y+=+q);f?(b+=y,"bottom"==d?(n.bottom+=b+t,a.box={top:B.height-n.bottom,height:b}):(a.box={top:n.top+t,height:b},n.top+=b+t)):(c+=y,"left"==d?(a.box={left:n.left+t,width:c},n.left+=c+t):(n.right+=c+t,a.box={left:B.width-n.right,width:c}));a.position=d;a.tickLength=q;a.box.padding=y;a.innermost=r}function na(){var a=e.grid.minBorderMargin,c;if(null==a)for(c=a=0;c<w.length;++c)a=Math.max(a,2*(w[c].points.radius+w[c].points.lineWidth/
 2));var b=a,d=a,f=a,q=a;m.each(F(),function(a,c){c.reserveSpace&&c.ticks&&c.ticks.length&&("x"===c.direction?(b=Math.max(b,c.labelWidth/2),d=Math.max(d,c.labelWidth/2)):(q=Math.max(q,c.labelHeight/2),f=Math.max(f,c.labelHeight/2)))});n.left=Math.ceil(Math.max(b,n.left));n.right=Math.ceil(Math.max(d,n.right));n.top=Math.ceil(Math.max(f,n.top));n.bottom=Math.ceil(Math.max(q,n.bottom))}function aa(){var a,c=F(),b=e.grid.show;for(a in n){var d=e.grid.margin||0;n[a]="number"==typeof d?d:d[a]||0}s(G.processOffset,
 [n]);for(a in n)n[a]="object"==typeof e.grid.borderWidth?n[a]+(b?e.grid.borderWidth[a]:0):n[a]+(b?e.grid.borderWidth:0);m.each(c,function(a,b){var c=b.options;b.show=null==c.show?b.used:c.show;b.reserveSpace=null==c.reserveSpace?b.show:c.reserveSpace;var c=b.options,d=+(null!=c.min?c.min:b.datamin),r=+(null!=c.max?c.max:b.datamax),e=r-d;if(0==e){if(e=0==r?1:.01,null==c.min&&(d-=e),null==c.max||null!=c.min)r+=e}else{var g=c.autoscaleMargin;null!=g&&(null==c.min&&(d-=e*g,0>d&&null!=b.datamin&&0<=b.datamin&&
 (d=0)),null==c.max&&(r+=e*g,0<r&&null!=b.datamax&&0>=b.datamax&&(r=0)))}b.min=d;b.max=r});if(b){d=m.grep(c,function(a){return a.show||a.reserveSpace});m.each(d,function(a,b){oa(b);var c=b.options.ticks,d=[];null==c||"number"==typeof c&&0<c?d=b.tickGenerator(b):c&&(d=m.isFunction(c)?c(b):c);var r;b.ticks=[];for(c=0;c<d.length;++c){var e=null,g=d[c];"object"==typeof g?(r=+g[0],1<g.length&&(e=g[1])):r=+g;null==e&&(e=b.tickFormatter(r,b));isNaN(r)||b.ticks.push({v:r,label:e})}d=b.ticks;b.options.autoscaleMargin&&
 0<d.length&&(null==b.options.min&&(b.min=Math.min(b.min,d[0].v)),null==b.options.max&&1<d.length&&(b.max=Math.max(b.max,d[d.length-1].v)));d=b.options;c=b.ticks||[];r=d.labelWidth||0;for(var e=d.labelHeight||0,g=r||("x"==b.direction?Math.floor(B.width/(c.length||1)):null),l="flot-"+b.direction+"-axis flot-"+b.direction+b.n+"-axis "+(b.direction+"Axis "+b.direction+b.n+"Axis"),k=d.font||"flot-tick-label tickLabel",n=0;n<c.length;++n){var h=c[n];h.label&&(h=B.getTextInfo(l,h.label,k,null,g),r=Math.max(r,
 h.width),e=Math.max(e,h.height))}b.labelWidth=d.labelWidth||r;b.labelHeight=d.labelHeight||e});for(a=d.length-1;0<=a;--a)ma(d[a]);na();m.each(d,function(a,b){"x"==b.direction?(b.box.left=n.left-b.labelWidth/2,b.box.width=B.width-n.left-n.right+b.labelWidth):(b.box.top=n.top-b.labelHeight/2,b.box.height=B.height-n.bottom-n.top+b.labelHeight)})}N=B.width-n.left-n.right;J=B.height-n.bottom-n.top;m.each(c,function(a,b){la(b)});b&&pa();qa()}function oa(a){var c=a.options,b;b="number"==typeof c.ticks&&
 0<c.ticks?c.ticks:.3*Math.sqrt("x"==a.direction?B.width:B.height);b=(a.max-a.min)/b;var d=-Math.floor(Math.log(b)/Math.LN10),f=c.tickDecimals;null!=f&&d>f&&(d=f);var e=Math.pow(10,-d),t=b/e,g;1.5>t?g=1:3>t?(g=2,2.25<t&&(null==f||d+1<=f)&&(g=2.5,++d)):g=7.5>t?5:10;g*=e;null!=c.minTickSize&&g<c.minTickSize&&(g=c.minTickSize);a.delta=b;a.tickDecimals=Math.max(0,null!=f?f:d);a.tickSize=c.tickSize||g;if("time"==c.mode&&!a.tickGenerator)throw Error("Time mode requires the flot.time plugin.");a.tickGenerator||
 (a.tickGenerator=function(a){var b=[],c;c=a.tickSize;c*=Math.floor(a.min/c);var d=0,f=Number.NaN,e;do e=f,f=c+d*a.tickSize,b.push(f),++d;while(f<a.max&&f!=e);return b},a.tickFormatter=function(a,b){var c=b.tickDecimals?Math.pow(10,b.tickDecimals):1,d=""+Math.round(a*c)/c;if(null!=b.tickDecimals){var f=d.indexOf("."),f=-1==f?0:d.length-f-1;if(f<b.tickDecimals)return(f?d:d+".")+(""+c).substr(1,b.tickDecimals-f)}return d});m.isFunction(c.tickFormatter)&&(a.tickFormatter=function(a,b){return""+c.tickFormatter(a,
 b)});if(null!=c.alignTicksWithAxis){var r=("x"==a.direction?E:I)[c.alignTicksWithAxis-1];r&&r.used&&r!=a&&(b=a.tickGenerator(a),0<b.length&&(null==c.min&&(a.min=Math.min(a.min,b[0])),null==c.max&&1<b.length&&(a.max=Math.max(a.max,b[b.length-1]))),a.tickGenerator=function(a){var b=[],c,d;for(d=0;d<r.ticks.length;++d)c=(r.ticks[d].v-r.min)/(r.max-r.min),c=a.min+c*(a.max-a.min),b.push(c);return b},a.mode||null!=c.tickDecimals||(b=Math.max(0,-Math.floor(Math.log(a.delta)/Math.LN10)+1),d=a.tickGenerator(a),
 1<d.length&&/\..*0$/.test((d[1]-d[0]).toFixed(b))||(a.tickDecimals=b)))}}function ba(){B.clear();s(G.drawBackground,[l]);var a=e.grid;a.show&&a.backgroundColor&&(l.save(),l.translate(n.left,n.top),l.fillStyle=ca(e.grid.backgroundColor,J,0,"rgba(255, 255, 255, 0)"),l.fillRect(0,0,N,J),l.restore());a.show&&!a.aboveData&&da();for(var c=0;c<w.length;++c){s(G.drawSeries,[l,w[c]]);var b=w[c];b.lines.show&&ra(b);b.bars.show&&sa(b);b.points.show&&ta(b)}s(G.draw,[l]);a.show&&a.aboveData&&da();B.render();S()}
 function ea(a,c){for(var b,d,f,e,g=F(),l=0;l<g.length;++l)if(b=g[l],b.direction==c&&(e=c+b.n+"axis",a[e]||1!=b.n||(e=c+"axis"),a[e])){d=a[e].from;f=a[e].to;break}a[e]||(b="x"==c?E[0]:I[0],d=a[c+"1"],f=a[c+"2"]);null!=d&&null!=f&&d>f&&(e=d,d=f,f=e);return{from:d,to:f,axis:b}}function da(){var a,c,b;l.save();l.translate(n.left,n.top);if(b=e.grid.markings)for(m.isFunction(b)&&(c=x.getAxes(),c.xmin=c.xaxis.min,c.xmax=c.xaxis.max,c.ymin=c.yaxis.min,c.ymax=c.yaxis.max,b=b(c)),a=0;a<b.length;++a){c=b[a];
 var d=ea(c,"x"),f=ea(c,"y");null==d.from&&(d.from=d.axis.min);null==d.to&&(d.to=d.axis.max);null==f.from&&(f.from=f.axis.min);null==f.to&&(f.to=f.axis.max);if(!(d.to<d.axis.min||d.from>d.axis.max||f.to<f.axis.min||f.from>f.axis.max)){d.from=Math.max(d.from,d.axis.min);d.to=Math.min(d.to,d.axis.max);f.from=Math.max(f.from,f.axis.min);f.to=Math.min(f.to,f.axis.max);var g=d.from===d.to,t=f.from===f.to;if(!g||!t)if(d.from=Math.floor(d.axis.p2c(d.from)),d.to=Math.floor(d.axis.p2c(d.to)),f.from=Math.floor(f.axis.p2c(f.from)),
 f.to=Math.floor(f.axis.p2c(f.to)),g||t){var t=c.lineWidth||e.grid.markingsLineWidth,k=t%2?.5:0;l.beginPath();l.strokeStyle=c.color||e.grid.markingsColor;l.lineWidth=t;g?(l.moveTo(d.to+k,f.from),l.lineTo(d.to+k,f.to)):(l.moveTo(d.from,f.to+k),l.lineTo(d.to,f.to+k));l.stroke()}else l.fillStyle=c.color||e.grid.markingsColor,l.fillRect(d.from,f.to,d.to-d.from,f.from-f.to)}}c=F();b=e.grid.borderWidth;for(d=0;d<c.length;++d){f=c[d];a=f.box;var g=f.tickLength,r,P;if(f.show&&0!=f.ticks.length){l.lineWidth=
 1;"x"==f.direction?(t=0,k="full"==g?"top"==f.position?0:J:a.top-n.top+("top"==f.position?a.height:0)):(k=0,t="full"==g?"left"==f.position?0:N:a.left-n.left+("left"==f.position?a.width:0));f.innermost||(l.strokeStyle=f.options.color,l.beginPath(),r=P=0,"x"==f.direction?r=N+1:P=J+1,1==l.lineWidth&&("x"==f.direction?k=Math.floor(k)+.5:t=Math.floor(t)+.5),l.moveTo(t,k),l.lineTo(t+r,k+P),l.stroke());l.strokeStyle=f.options.tickColor;l.beginPath();for(a=0;a<f.ticks.length;++a){var h=f.ticks[a].v;r=P=0;
 isNaN(h)||h<f.min||h>f.max||"full"==g&&("object"==typeof b&&0<b[f.position]||0<b)&&(h==f.min||h==f.max)||("x"==f.direction?(t=f.p2c(h),P="full"==g?-J:g,"top"==f.position&&(P=-P)):(k=f.p2c(h),r="full"==g?-N:g,"left"==f.position&&(r=-r)),1==l.lineWidth&&("x"==f.direction?t=Math.floor(t)+.5:k=Math.floor(k)+.5),l.moveTo(t,k),l.lineTo(t+r,k+P))}l.stroke()}}b&&(a=e.grid.borderColor,"object"==typeof b||"object"==typeof a?("object"!==typeof b&&(b={top:b,right:b,bottom:b,left:b}),"object"!==typeof a&&(a={top:a,
 right:a,bottom:a,left:a}),0<b.top&&(l.strokeStyle=a.top,l.lineWidth=b.top,l.beginPath(),l.moveTo(0-b.left,0-b.top/2),l.lineTo(N,0-b.top/2),l.stroke()),0<b.right&&(l.strokeStyle=a.right,l.lineWidth=b.right,l.beginPath(),l.moveTo(N+b.right/2,0-b.top),l.lineTo(N+b.right/2,J),l.stroke()),0<b.bottom&&(l.strokeStyle=a.bottom,l.lineWidth=b.bottom,l.beginPath(),l.moveTo(N+b.right,J+b.bottom/2),l.lineTo(0,J+b.bottom/2),l.stroke()),0<b.left&&(l.strokeStyle=a.left,l.lineWidth=b.left,l.beginPath(),l.moveTo(0-
 b.left/2,J+b.bottom),l.lineTo(0-b.left/2,0),l.stroke())):(l.lineWidth=b,l.strokeStyle=e.grid.borderColor,l.strokeRect(-b/2,-b/2,N+b,J+b)));l.restore()}function pa(){m.each(F(),function(a,c){var b=c.box,d="flot-"+c.direction+"-axis flot-"+c.direction+c.n+"-axis "+(c.direction+"Axis "+c.direction+c.n+"Axis"),f=c.options.font||"flot-tick-label tickLabel",e,g,l,r,k;B.removeText(d);if(c.show&&0!=c.ticks.length)for(var h=0;h<c.ticks.length;++h)e=c.ticks[h],!e.label||e.v<c.min||e.v>c.max||("x"==c.direction?
 (r="center",g=n.left+c.p2c(e.v),"bottom"==c.position?l=b.top+b.padding:(l=b.top+b.height-b.padding,k="bottom")):(k="middle",l=n.top+c.p2c(e.v),"left"==c.position?(g=b.left+b.width-b.padding,r="right"):g=b.left+b.padding),B.addText(d,g,l,e.label,f,null,null,r,k))})}function ra(a){function c(a,b,c,d,f){var e=a.points;a=a.pointsize;var g=null,k=null;l.beginPath();for(var h=a;h<e.length;h+=a){var n=e[h-a],v=e[h-a+1],m=e[h],q=e[h+1];if(null!=n&&null!=m){if(v<=q&&v<f.min){if(q<f.min)continue;n=(f.min-v)/
 (q-v)*(m-n)+n;v=f.min}else if(q<=v&&q<f.min){if(v<f.min)continue;m=(f.min-v)/(q-v)*(m-n)+n;q=f.min}if(v>=q&&v>f.max){if(q>f.max)continue;n=(f.max-v)/(q-v)*(m-n)+n;v=f.max}else if(q>=v&&q>f.max){if(v>f.max)continue;m=(f.max-v)/(q-v)*(m-n)+n;q=f.max}if(n<=m&&n<d.min){if(m<d.min)continue;v=(d.min-n)/(m-n)*(q-v)+v;n=d.min}else if(m<=n&&m<d.min){if(n<d.min)continue;q=(d.min-n)/(m-n)*(q-v)+v;m=d.min}if(n>=m&&n>d.max){if(m>d.max)continue;v=(d.max-n)/(m-n)*(q-v)+v;n=d.max}else if(m>=n&&m>d.max){if(n>d.max)continue;
 q=(d.max-n)/(m-n)*(q-v)+v;m=d.max}n==g&&v==k||l.moveTo(d.p2c(n)+b,f.p2c(v)+c);g=m;k=q;l.lineTo(d.p2c(m)+b,f.p2c(q)+c)}}l.stroke()}function b(a,b,c){var d=a.points;a=a.pointsize;for(var f=Math.min(Math.max(0,c.min),c.max),e=0,g=!1,k=1,n=0,m=0;!(0<a&&e>d.length+a);){var e=e+a,h=d[e-a],q=d[e-a+k],p=d[e],s=d[e+k];if(g){if(0<a&&null!=h&&null==p){m=e;a=-a;k=2;continue}if(0>a&&e==n+a){l.fill();g=!1;a=-a;k=1;e=n=m+a;continue}}if(null!=h&&null!=p){if(h<=p&&h<b.min){if(p<b.min)continue;q=(b.min-h)/(p-h)*(s-
 q)+q;h=b.min}else if(p<=h&&p<b.min){if(h<b.min)continue;s=(b.min-h)/(p-h)*(s-q)+q;p=b.min}if(h>=p&&h>b.max){if(p>b.max)continue;q=(b.max-h)/(p-h)*(s-q)+q;h=b.max}else if(p>=h&&p>b.max){if(h>b.max)continue;s=(b.max-h)/(p-h)*(s-q)+q;p=b.max}g||(l.beginPath(),l.moveTo(b.p2c(h),c.p2c(f)),g=!0);if(q>=c.max&&s>=c.max)l.lineTo(b.p2c(h),c.p2c(c.max)),l.lineTo(b.p2c(p),c.p2c(c.max));else if(q<=c.min&&s<=c.min)l.lineTo(b.p2c(h),c.p2c(c.min)),l.lineTo(b.p2c(p),c.p2c(c.min));else{var w=h,x=p;q<=s&&q<c.min&&s>=
 c.min?(h=(c.min-q)/(s-q)*(p-h)+h,q=c.min):s<=q&&s<c.min&&q>=c.min&&(p=(c.min-q)/(s-q)*(p-h)+h,s=c.min);q>=s&&q>c.max&&s<=c.max?(h=(c.max-q)/(s-q)*(p-h)+h,q=c.max):s>=q&&s>c.max&&q<=c.max&&(p=(c.max-q)/(s-q)*(p-h)+h,s=c.max);h!=w&&l.lineTo(b.p2c(w),c.p2c(q));l.lineTo(b.p2c(h),c.p2c(q));l.lineTo(b.p2c(p),c.p2c(s));p!=x&&(l.lineTo(b.p2c(p),c.p2c(s)),l.lineTo(b.p2c(x),c.p2c(s)))}}}}l.save();l.translate(n.left,n.top);l.lineJoin="round";var d=a.lines.lineWidth,f=a.shadowSize;if(0<d&&0<f){l.lineWidth=f;
 l.strokeStyle="rgba(0,0,0,0.1)";var e=Math.PI/18;c(a.datapoints,Math.sin(e)*(d/2+f/2),Math.cos(e)*(d/2+f/2),a.xaxis,a.yaxis);l.lineWidth=f/2;c(a.datapoints,Math.sin(e)*(d/2+f/4),Math.cos(e)*(d/2+f/4),a.xaxis,a.yaxis)}l.lineWidth=d;l.strokeStyle=a.color;if(f=U(a.lines,a.color,0,J))l.fillStyle=f,b(a.datapoints,a.xaxis,a.yaxis);0<d&&c(a.datapoints,0,0,a.xaxis,a.yaxis);l.restore()}function ta(a){function c(a,b,c,d,f,e,g,k){var h=a.points;a=a.pointsize;for(var n=0;n<h.length;n+=a){var q=h[n],m=h[n+1];
 null==q||q<e.min||q>e.max||m<g.min||m>g.max||(l.beginPath(),q=e.p2c(q),m=g.p2c(m)+d,"circle"==k?l.arc(q,m,b,0,f?Math.PI:2*Math.PI,!1):k(l,q,m,b,f),l.closePath(),c&&(l.fillStyle=c,l.fill()),l.stroke())}}l.save();l.translate(n.left,n.top);var b=a.points.lineWidth,d=a.shadowSize,f=a.points.radius,e=a.points.symbol;0==b&&(b=1E-4);0<b&&0<d&&(d/=2,l.lineWidth=d,l.strokeStyle="rgba(0,0,0,0.1)",c(a.datapoints,f,null,d+d/2,!0,a.xaxis,a.yaxis,e),l.strokeStyle="rgba(0,0,0,0.2)",c(a.datapoints,f,null,d/2,!0,
 a.xaxis,a.yaxis,e));l.lineWidth=b;l.strokeStyle=a.color;c(a.datapoints,f,U(a.points,a.color),0,!1,a.xaxis,a.yaxis,e);l.restore()}function fa(a,c,b,d,f,e,g,k,l,h,n){var m,p,s,w;h?(w=p=s=!0,m=!1,h=b,b=c+d,f=c+f,a<h&&(c=a,a=h,h=c,m=!0,p=!1)):(m=p=s=!0,w=!1,h=a+d,a+=f,f=b,b=c,b<f&&(c=b,b=f,f=c,w=!0,s=!1));a<g.min||h>g.max||b<k.min||f>k.max||(h<g.min&&(h=g.min,m=!1),a>g.max&&(a=g.max,p=!1),f<k.min&&(f=k.min,w=!1),b>k.max&&(b=k.max,s=!1),h=g.p2c(h),f=k.p2c(f),a=g.p2c(a),b=k.p2c(b),e&&(l.fillStyle=e(f,b),
 l.fillRect(h,b,a-h,f-b)),0<n&&(m||p||s||w)&&(l.beginPath(),l.moveTo(h,f),m?l.lineTo(h,b):l.moveTo(h,b),s?l.lineTo(a,b):l.moveTo(a,b),p?l.lineTo(a,f):l.moveTo(a,f),w?l.lineTo(h,f):l.moveTo(h,f),l.stroke()))}function sa(a){l.save();l.translate(n.left,n.top);l.lineWidth=a.bars.lineWidth;l.strokeStyle=a.color;var c;switch(a.bars.align){case "left":c=0;break;case "right":c=-a.bars.barWidth;break;default:c=-a.bars.barWidth/2}(function(b,c,f,e,g,h){var k=b.points;b=b.pointsize;for(var n=0;n<k.length;n+=
 b)null!=k[n]&&fa(k[n],k[n+1],k[n+2],c,f,e,g,h,l,a.bars.horizontal,a.bars.lineWidth)})(a.datapoints,c,c+a.bars.barWidth,a.bars.fill?function(b,c){return U(a.bars,a.color,b,c)}:null,a.xaxis,a.yaxis);l.restore()}function U(a,c,b,d){var f=a.fill;if(!f)return null;if(a.fillColor)return ca(a.fillColor,b,d,c);a=m.color.parse(c);a.a="number"==typeof f?f:.4;a.normalize();return a.toString()}function qa(){null!=e.legend.container?m(e.legend.container).html(""):g.find(".legend").remove();if(e.legend.show){for(var a=
 [],c=[],b=!1,d=e.legend.labelFormatter,f,k,h=0;h<w.length;++h)f=w[h],f.label&&(k=d?d(f.label,f):f.label)&&c.push({label:k,color:f.color});if(e.legend.sorted)if(m.isFunction(e.legend.sorted))c.sort(e.legend.sorted);else if("reverse"==e.legend.sorted)c.reverse();else{var l="descending"!=e.legend.sorted;c.sort(function(a,b){return a.label==b.label?0:a.label<b.label!=l?1:-1})}for(h=0;h<c.length;++h)d=c[h],0==h%e.legend.noColumns&&(b&&a.push("</tr>"),a.push("<tr>"),b=!0),a.push('<td class="legendColorBox"><div style="border:1px solid '+
 e.legend.labelBoxBorderColor+';padding:1px"><div style="width:4px;height:0;border:5px solid '+d.color+';overflow:hidden"></div></div></td><td class="legendLabel">'+d.label+"</td>");b&&a.push("</tr>");0!=a.length&&(c='<table style="font-size:smaller;color:'+e.grid.color+'">'+a.join("")+"</table>",null!=e.legend.container?m(e.legend.container).html(c):(a="",b=e.legend.position,h=e.legend.margin,null==h[0]&&(h=[h,h]),"n"==b.charAt(0)?a+="top:"+(h[1]+n.top)+"px;":"s"==b.charAt(0)&&(a+="bottom:"+(h[1]+
 n.bottom)+"px;"),"e"==b.charAt(1)?a+="right:"+(h[0]+n.right)+"px;":"w"==b.charAt(1)&&(a+="left:"+(h[0]+n.left)+"px;"),c=m('<div class="legend">'+c.replace('style="','style="position:absolute;'+a+";")+"</div>").appendTo(g),0!=e.legend.backgroundOpacity&&(b=e.legend.backgroundColor,null==b&&(b=(b=e.grid.backgroundColor)&&"string"==typeof b?m.color.parse(b):m.color.extract(c,"background-color"),b.a=1,b=b.toString()),h=c.children(),m('<div style="position:absolute;width:'+h.width()+"px;height:"+h.height()+
 "px;"+a+"background-color:"+b+';"> </div>').prependTo(c).css("opacity",e.legend.backgroundOpacity))))}}function Y(a){e.grid.hoverable&&V("plothover",a,function(a){return!1!=a.hoverable})}function Z(a){e.grid.hoverable&&V("plothover",a,function(a){return!1})}function $(a){V("plotclick",a,function(a){return!1!=a.clickable})}function V(a,c,b){var d=M.offset(),f=c.pageX-d.left-n.left,h=c.pageY-d.top-n.top,k=W({left:f,top:h});k.pageX=c.pageX;k.pageY=c.pageY;c=e.grid.mouseActiveRadius;var l=c*c+1,m=null,
 p,s,x;for(p=w.length-1;0<=p;--p)if(b(w[p])){var H=w[p],u=H.xaxis,K=H.yaxis,D=H.datapoints.points,v=u.c2p(f),B=K.c2p(h),F=c/u.scale,E=c/K.scale;x=H.datapoints.pointsize;u.options.inverseTransform&&(F=Number.MAX_VALUE);K.options.inverseTransform&&(E=Number.MAX_VALUE);if(H.lines.show||H.points.show)for(s=0;s<D.length;s+=x){var A=D[s],z=D[s+1];null==A||A-v>F||A-v<-F||z-B>E||z-B<-E||(A=Math.abs(u.p2c(A)-f),z=Math.abs(K.p2c(z)-h),z=A*A+z*z,z<l&&(l=z,m=[p,s/x]))}if(H.bars.show&&!m){switch(H.bars.align){case "left":u=
 0;break;case "right":u=-H.bars.barWidth;break;default:u=-H.bars.barWidth/2}H=u+H.bars.barWidth;for(s=0;s<D.length;s+=x)A=D[s],z=D[s+1],K=D[s+2],null!=A&&(w[p].bars.horizontal?v<=Math.max(K,A)&&v>=Math.min(K,A)&&B>=z+u&&B<=z+H:v>=A+u&&v<=A+H&&B>=Math.min(K,z)&&B<=Math.max(K,z))&&(m=[p,s/x])}}m?(p=m[0],s=m[1],x=w[p].datapoints.pointsize,b={datapoint:w[p].datapoints.points.slice(s*x,(s+1)*x),dataIndex:s,series:w[p],seriesIndex:p}):b=null;b&&(b.pageX=parseInt(b.series.xaxis.p2c(b.datapoint[0])+d.left+
 n.left,10),b.pageY=parseInt(b.series.yaxis.p2c(b.datapoint[1])+d.top+n.top,10));if(e.grid.autoHighlight){for(d=0;d<O.length;++d)f=O[d],f.auto!=a||b&&f.series==b.series&&f.point[0]==b.datapoint[0]&&f.point[1]==b.datapoint[1]||ga(f.series,f.point);b&&ha(b.series,b.datapoint,a)}g.trigger(a,[k,b])}function S(){var a=e.interaction.redrawOverlayInterval;-1==a?ia():R||(R=setTimeout(ia,a))}function ia(){R=null;A.save();Q.clear();A.translate(n.left,n.top);var a,c;for(a=0;a<O.length;++a)if(c=O[a],c.series.bars.show)ua(c.series,
 c.point);else{var b=c.series,d=c.point;c=d[0];var d=d[1],f=b.xaxis,e=b.yaxis,g="string"===typeof b.highlightColor?b.highlightColor:m.color.parse(b.color).scale("a",.5).toString();if(!(c<f.min||c>f.max||d<e.min||d>e.max)){var h=b.points.radius+b.points.lineWidth/2;A.lineWidth=h;A.strokeStyle=g;g=1.5*h;c=f.p2c(c);d=e.p2c(d);A.beginPath();"circle"==b.points.symbol?A.arc(c,d,g,0,2*Math.PI,!1):b.points.symbol(A,c,d,g,!1);A.closePath();A.stroke()}}A.restore();s(G.drawOverlay,[A])}function ha(a,c,b){"number"==
 typeof a&&(a=w[a]);if("number"==typeof c){var d=a.datapoints.pointsize;c=a.datapoints.points.slice(d*c,d*(c+1))}d=ja(a,c);-1==d?(O.push({series:a,point:c,auto:b}),S()):b||(O[d].auto=!1)}function ga(a,c){if(null==a&&null==c)O=[],S();else{"number"==typeof a&&(a=w[a]);if("number"==typeof c){var b=a.datapoints.pointsize;c=a.datapoints.points.slice(b*c,b*(c+1))}b=ja(a,c);-1!=b&&(O.splice(b,1),S())}}function ja(a,c){for(var b=0;b<O.length;++b){var d=O[b];if(d.series==a&&d.point[0]==c[0]&&d.point[1]==c[1])return b}return-1}
 function ua(a,c){var b="string"===typeof a.highlightColor?a.highlightColor:m.color.parse(a.color).scale("a",.5).toString(),d;switch(a.bars.align){case "left":d=0;break;case "right":d=-a.bars.barWidth;break;default:d=-a.bars.barWidth/2}A.lineWidth=a.bars.lineWidth;A.strokeStyle=b;fa(c[0],c[1],c[2]||0,d,d+a.bars.barWidth,function(){return b},a.xaxis,a.yaxis,A,a.bars.horizontal,a.bars.lineWidth)}function ca(a,c,b,d){if("string"==typeof a)return a;c=l.createLinearGradient(0,b,0,c);b=0;for(var f=a.colors.length;b<
 f;++b){var e=a.colors[b];if("string"!=typeof e){var g=m.color.parse(d);null!=e.brightness&&(g=g.scale("rgb",e.brightness));null!=e.opacity&&(g.a*=e.opacity);e=g.toString()}c.addColorStop(b/(f-1),e)}return c}var w=[],e={colors:["#edc240","#afd8f8","#cb4b4b","#4da74d","#9440ed"],legend:{show:!0,noColumns:1,labelFormatter:null,labelBoxBorderColor:"#ccc",container:null,position:"ne",margin:5,backgroundColor:null,backgroundOpacity:.85,sorted:null},xaxis:{show:null,position:"bottom",mode:null,font:null,
 color:null,tickColor:null,transform:null,inverseTransform:null,min:null,max:null,autoscaleMargin:null,ticks:null,tickFormatter:null,labelWidth:null,labelHeight:null,reserveSpace:null,tickLength:null,alignTicksWithAxis:null,tickDecimals:null,tickSize:null,minTickSize:null},yaxis:{autoscaleMargin:.02,position:"left"},xaxes:[],yaxes:[],series:{points:{show:!1,radius:3,lineWidth:2,fill:!0,fillColor:"#ffffff",symbol:"circle"},lines:{lineWidth:2,fill:!1,fillColor:null,steps:!1},bars:{show:!1,lineWidth:2,
 barWidth:1,fill:!0,fillColor:null,align:"left",horizontal:!1,zero:!0},shadowSize:3,highlightColor:null},grid:{show:!0,aboveData:!1,color:"#545454",backgroundColor:null,borderColor:null,tickColor:null,margin:0,labelMargin:5,axisMargin:8,borderWidth:2,minBorderMargin:null,markings:null,markingsColor:"#f4f4f4",markingsLineWidth:2,clickable:!1,hoverable:!1,autoHighlight:!0,mouseActiveRadius:10},interaction:{redrawOverlayInterval:1E3/60},hooks:{}},B=null,Q=null,M=null,l=null,A=null,E=[],I=[],n={left:0,
 right:0,top:0,bottom:0},N=0,J=0,G={processOptions:[],processRawData:[],processDatapoints:[],processOffset:[],drawBackground:[],drawSeries:[],draw:[],bindEvents:[],drawOverlay:[],shutdown:[]},x=this;x.setData=K;x.setupGrid=aa;x.draw=ba;x.getPlaceholder=function(){return g};x.getCanvas=function(){return B.element};x.getPlotOffset=function(){return n};x.width=function(){return N};x.height=function(){return J};x.offset=function(){var a=M.offset();a.left+=n.left;a.top+=n.top;return a};x.getData=function(){return w};
 x.getAxes=function(){var a={};m.each(E.concat(I),function(c,b){b&&(a[b.direction+(1!=b.n?b.n:"")+"axis"]=b)});return a};x.getXAxes=function(){return E};x.getYAxes=function(){return I};x.c2p=W;x.p2c=function(a){var c={},b,d,e;for(b=0;b<E.length;++b)if((d=E[b])&&d.used&&(e="x"+d.n,null==a[e]&&1==d.n&&(e="x"),null!=a[e])){c.left=d.p2c(a[e]);break}for(b=0;b<I.length;++b)if((d=I[b])&&d.used&&(e="y"+d.n,null==a[e]&&1==d.n&&(e="y"),null!=a[e])){c.top=d.p2c(a[e]);break}return c};x.getOptions=function(){return e};
 x.highlight=ha;x.unhighlight=ga;x.triggerRedrawOverlay=S;x.pointOffset=function(a){return{left:parseInt(E[u(a,"x")-1].p2c(+a.x)+n.left,10),top:parseInt(I[u(a,"y")-1].p2c(+a.y)+n.top,10)}};x.shutdown=X;x.destroy=function(){X();g.removeData("plot").empty();w=[];A=l=M=Q=B=e=null;E=[];I=[];G=null;O=[];x=null};x.resize=function(){var a=g.width(),c=g.height();B.resize(a,c);Q.resize(a,c)};x.hooks=G;(function(){for(var a={Canvas:C},c=0;c<p.length;++c){var b=p[c];b.init(x,a);b.options&&m.extend(!0,e,b.options)}})(x);
 (function(a){m.extend(!0,e,a);a&&a.colors&&(e.colors=a.colors);null==e.xaxis.color&&(e.xaxis.color=m.color.parse(e.grid.color).scale("a",.22).toString());null==e.yaxis.color&&(e.yaxis.color=m.color.parse(e.grid.color).scale("a",.22).toString());null==e.xaxis.tickColor&&(e.xaxis.tickColor=e.grid.tickColor||e.xaxis.color);null==e.yaxis.tickColor&&(e.yaxis.tickColor=e.grid.tickColor||e.yaxis.color);null==e.grid.borderColor&&(e.grid.borderColor=e.grid.color);null==e.grid.tickColor&&(e.grid.tickColor=
 m.color.parse(e.grid.color).scale("a",.22).toString());var c,b;a=(a=g.css("font-size"))?+a.replace("px",""):13;var d={style:g.css("font-style"),size:Math.round(.8*a),variant:g.css("font-variant"),weight:g.css("font-weight"),family:g.css("font-family")};b=e.xaxes.length||1;for(a=0;a<b;++a)(c=e.xaxes[a])&&!c.tickColor&&(c.tickColor=c.color),c=m.extend(!0,{},e.xaxis,c),e.xaxes[a]=c,c.font&&(c.font=m.extend({},d,c.font),c.font.color||(c.font.color=c.color),c.font.lineHeight||(c.font.lineHeight=Math.round(1.15*
 c.font.size)));b=e.yaxes.length||1;for(a=0;a<b;++a)(c=e.yaxes[a])&&!c.tickColor&&(c.tickColor=c.color),c=m.extend(!0,{},e.yaxis,c),e.yaxes[a]=c,c.font&&(c.font=m.extend({},d,c.font),c.font.color||(c.font.color=c.color),c.font.lineHeight||(c.font.lineHeight=Math.round(1.15*c.font.size)));e.xaxis.noTicks&&null==e.xaxis.ticks&&(e.xaxis.ticks=e.xaxis.noTicks);e.yaxis.noTicks&&null==e.yaxis.ticks&&(e.yaxis.ticks=e.yaxis.noTicks);e.x2axis&&(e.xaxes[1]=m.extend(!0,{},e.xaxis,e.x2axis),e.xaxes[1].position=
 "top",null==e.x2axis.min&&(e.xaxes[1].min=null),null==e.x2axis.max&&(e.xaxes[1].max=null));e.y2axis&&(e.yaxes[1]=m.extend(!0,{},e.yaxis,e.y2axis),e.yaxes[1].position="right",null==e.y2axis.min&&(e.yaxes[1].min=null),null==e.y2axis.max&&(e.yaxes[1].max=null));e.grid.coloredAreas&&(e.grid.markings=e.grid.coloredAreas);e.grid.coloredAreasColor&&(e.grid.markingsColor=e.grid.coloredAreasColor);e.lines&&m.extend(!0,e.series.lines,e.lines);e.points&&m.extend(!0,e.series.points,e.points);e.bars&&m.extend(!0,
 e.series.bars,e.bars);null!=e.shadowSize&&(e.series.shadowSize=e.shadowSize);null!=e.highlightColor&&(e.series.highlightColor=e.highlightColor);for(a=0;a<e.xaxes.length;++a)L(E,a+1).options=e.xaxes[a];for(a=0;a<e.yaxes.length;++a)L(I,a+1).options=e.yaxes[a];for(var f in G)e.hooks[f]&&e.hooks[f].length&&(G[f]=G[f].concat(e.hooks[f]));s(G.processOptions,[e])})(k);(function(){g.css("padding",0).children().filter(function(){return!m(this).hasClass("flot-overlay")&&!m(this).hasClass("flot-base")}).remove();
 "static"==g.css("position")&&g.css("position","relative");B=new C("flot-base",g);Q=new C("flot-overlay",g);l=B.context;A=Q.context;M=m(Q.element).unbind();var a=g.data("plot");a&&(a.shutdown(),Q.clear());g.data("plot",x)})();K(h);aa();ba();e.grid.hoverable&&(M.mousemove(Y),M.bind("mouseleave",Z));e.grid.clickable&&M.click($);s(G.bindEvents,[M]);var O=[],R=null}var p=Object.prototype.hasOwnProperty;m.fn.detach||(m.fn.detach=function(){return this.each(function(){this.parentNode&&this.parentNode.removeChild(this)})});
 C.prototype.resize=function(g,h){if(0>=g||0>=h)throw Error("Invalid dimensions for plot, width = "+g+", height = "+h);var k=this.element,m=this.context,p=this.pixelRatio;this.width!=g&&(k.width=g*p,k.style.width=g+"px",this.width=g);this.height!=h&&(k.height=h*p,k.style.height=h+"px",this.height=h);m.restore();m.save();m.scale(p,p)};C.prototype.clear=function(){this.context.clearRect(0,0,this.width,this.height)};C.prototype.render=function(){var g=this._textCache,h;for(h in g)if(p.call(g,h)){var k=
 this.getTextLayer(h),m=g[h];k.hide();for(var s in m)if(p.call(m,s)){var u=m[s],z;for(z in u)if(p.call(u,z)){for(var F=u[z].positions,C=0,L;L=F[C];C++)L.active?L.rendered||(k.append(L.element),L.rendered=!0):(F.splice(C--,1),L.rendered&&L.element.detach());0==F.length&&delete u[z]}}k.show()}};C.prototype.getTextLayer=function(g){var h=this.text[g];null==h&&(null==this.textContainer&&(this.textContainer=m("<div class='flot-text'></div>").css({position:"absolute",top:0,left:0,bottom:0,right:0,"font-size":"smaller",
 color:"#545454"}).insertAfter(this.element)),h=this.text[g]=m("<div></div>").addClass(g).css({position:"absolute",top:0,left:0,bottom:0,right:0}).appendTo(this.textContainer));return h};C.prototype.getTextInfo=function(g,h,k,p,s){var u,z;h=""+h;p="object"===typeof k?k.style+" "+k.variant+" "+k.weight+" "+k.size+"px/"+k.lineHeight+"px "+k.family:k;u=this._textCache[g];null==u&&(u=this._textCache[g]={});z=u[p];null==z&&(z=u[p]={});u=z[h];null==u&&(g=m("<div></div>").html(h).css({position:"absolute",
 "max-width":s,top:-9999}).appendTo(this.getTextLayer(g)),"object"===typeof k?g.css({font:p,color:k.color}):"string"===typeof k&&g.addClass(k),u=z[h]={width:g.outerWidth(!0),height:g.outerHeight(!0),element:g,positions:[]},g.detach());return u};C.prototype.addText=function(g,h,k,m,p,u,z,F,C){g=this.getTextInfo(g,m,p,u,z);m=g.positions;"center"==F?h-=g.width/2:"right"==F&&(h-=g.width);"middle"==C?k-=g.height/2:"bottom"==C&&(k-=g.height);for(C=0;p=m[C];C++)if(p.x==h&&p.y==k){p.active=!0;return}p={active:!0,
 rendered:!1,element:m.length?g.element.clone():g.element,x:h,y:k};m.push(p);p.element.css({top:Math.round(k),left:Math.round(h),"text-align":F})};C.prototype.removeText=function(g,h,k,m,s,u){if(null==m){if(h=this._textCache[g],null!=h)for(var z in h)if(p.call(h,z)){k=h[z];for(var C in k)if(p.call(k,C))for(g=k[C].positions,m=0;s=g[m];m++)s.active=!1}}else for(g=this.getTextInfo(g,m,s,u).positions,m=0;s=g[m];m++)s.x==h&&s.y==k&&(s.active=!1)};m.plot=function(g,h,k){return new u(m(g),h,k,m.plot.plugins)};
 m.plot.version="0.8.3";m.plot.plugins=[];m.fn.plot=function(g,h){return this.each(function(){m.plot(this,g,h)})}})(jQuery);
 */
(function (m) {
    m.color = {};
    m.color.make = function (u, p, g, h) {
        var k = {};
        k.r = u || 0;
        k.g = p || 0;
        k.b = g || 0;
        k.a = null != h ? h : 1;
        k.add = function (g, m) {
            for (var h = 0; h < g.length; ++h) k[g.charAt(h)] += m;
            return k.normalize()
        };
        k.scale = function (g, m) {
            for (var h = 0; h < g.length; ++h) k[g.charAt(h)] *= m;
            return k.normalize()
        };
        k.toString = function () {
            return 1 <= k.a ? "rgb(" + [k.r, k.g, k.b].join() + ")" : "rgba(" + [k.r, k.g, k.b, k.a].join() + ")"
        };
        k.normalize = function () {
            function g(k, m, h) {
                return m < k ? k : m > h ? h : m
            }

            k.r = g(0, parseInt(k.r), 255);
            k.g = g(0, parseInt(k.g), 255);
            k.b = g(0, parseInt(k.b), 255);
            k.a = g(0, k.a, 1);
            return k
        };
        k.clone = function () {
            return m.color.make(k.r, k.b, k.g, k.a)
        };
        return k.normalize()
    };
    m.color.extract = function (u, p) {
        var g;
        do {
            g = u.css(p).toLowerCase();
            if ("" != g && "transparent" != g) break;
            u = u.parent()
        } while (u.length && !m.nodeName(u.get(0), "body"));
        "rgba(0, 0, 0, 0)" == g && (g = "transparent");
        return m.color.parse(g)
    };
    m.color.parse = function (u) {
        var p, g = m.color.make;
        if (p = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(u)) return g(parseInt(p[1],
            10), parseInt(p[2], 10), parseInt(p[3], 10));
        if (p = /rgba\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(u)) return g(parseInt(p[1], 10), parseInt(p[2], 10), parseInt(p[3], 10), parseFloat(p[4]));
        if (p = /rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(u)) return g(2.55 * parseFloat(p[1]), 2.55 * parseFloat(p[2]), 2.55 * parseFloat(p[3]));
        if (p = /rgba\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)/.exec(u)) return g(2.55 *
            parseFloat(p[1]), 2.55 * parseFloat(p[2]), 2.55 * parseFloat(p[3]), parseFloat(p[4]));
        if (p = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(u)) return g(parseInt(p[1], 16), parseInt(p[2], 16), parseInt(p[3], 16));
        if (p = /#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(u)) return g(parseInt(p[1] + p[1], 16), parseInt(p[2] + p[2], 16), parseInt(p[3] + p[3], 16));
        u = m.trim(u).toLowerCase();
        if ("transparent" == u) return g(255, 255, 255, 0);
        p = C[u] || [0, 0, 0];
        return g(p[0], p[1], p[2])
    };
    var C = {
        aqua: [0, 255, 255],
        azure: [240, 255, 255],
        beige: [245,
            245, 220
        ],
        black: [0, 0, 0],
        blue: [0, 0, 255],
        brown: [165, 42, 42],
        cyan: [0, 255, 255],
        darkblue: [0, 0, 139],
        darkcyan: [0, 139, 139],
        darkgrey: [169, 169, 169],
        darkgreen: [0, 100, 0],
        darkkhaki: [189, 183, 107],
        darkmagenta: [139, 0, 139],
        darkolivegreen: [85, 107, 47],
        darkorange: [255, 140, 0],
        darkorchid: [153, 50, 204],
        darkred: [139, 0, 0],
        darksalmon: [233, 150, 122],
        darkviolet: [148, 0, 211],
        fuchsia: [255, 0, 255],
        gold: [255, 215, 0],
        green: [0, 128, 0],
        indigo: [75, 0, 130],
        khaki: [240, 230, 140],
        lightblue: [173, 216, 230],
        lightcyan: [224, 255, 255],
        lightgreen: [144, 238,
            144
        ],
        lightgrey: [211, 211, 211],
        lightpink: [255, 182, 193],
        lightyellow: [255, 255, 224],
        lime: [0, 255, 0],
        magenta: [255, 0, 255],
        maroon: [128, 0, 0],
        navy: [0, 0, 128],
        olive: [128, 128, 0],
        orange: [255, 165, 0],
        pink: [255, 192, 203],
        purple: [128, 0, 128],
        violet: [128, 0, 128],
        red: [255, 0, 0],
        silver: [192, 192, 192],
        white: [255, 255, 255],
        yellow: [255, 255, 0]
    }
})(jQuery);
(function (m) {
    function C(g, h) {
        var k = h.children("." + g)[0];
        if (null == k && (k = document.createElement("canvas"), k.className = g, m(k).css({
                direction: "ltr",
                position: "absolute",
                left: 0,
                top: 0
            }).appendTo(h), !k.getContext))
            if (window.G_vmlCanvasManager) k = window.G_vmlCanvasManager.initElement(k);
            else throw Error("Canvas is not available. If you're using IE with a fall-back such as Excanvas, then there's either a mistake in your conditional include, or the page has no DOCTYPE and is rendering in Quirks Mode.");
        this.element =
            k;
        k = this.context = k.getContext("2d");
        this.pixelRatio = (window.devicePixelRatio || 1) / (k.webkitBackingStorePixelRatio || k.mozBackingStorePixelRatio || k.msBackingStorePixelRatio || k.oBackingStorePixelRatio || k.backingStorePixelRatio || 1);
        this.resize(h.width(), h.height());
        this.textContainer = null;
        this.text = {};
        this._textCache = {}
    }

    function u(g, h, k, p) {
        function s(a, c) {
            c = [x].concat(c);
            for (var b = 0; b < a.length; ++b) a[b].apply(this, c)
        }

        function K(a) {
            for (var c = [], b = 0; b < a.length; ++b) {
                var d = m.extend(!0, {}, e.series);
                null != a[b].data ?
                    (d.data = a[b].data, delete a[b].data, m.extend(!0, d, a[b]), a[b].data = d.data) : d.data = a[b];
                c.push(d)
            }
            w = c;
            b = w.length;
            c = -1;
            for (a = 0; a < w.length; ++a) d = w[a].color, null != d && (b--, "number" == typeof d && d > c && (c = d));
            b <= c && (b = c + 1);
            var c = [],
                f = e.colors,
                q = f.length,
                t = 0;
            for (a = 0; a < b; a++) d = m.color.parse(f[a % q] || "#666"), 0 == a % q && a && (t = 0 <= t ? .5 > t ? -t - .2 : 0 : -t), c[a] = d.scale("rgb", 1 + t);
            for (a = b = 0; a < w.length; ++a) {
                d = w[a];
                null == d.color ? (d.color = c[b].toString(), ++b) : "number" == typeof d.color && (d.color = c[d.color].toString());
                if (null == d.lines.show) {
                    var y,
                        f = !0;
                    for (y in d)
                        if (d[y] && d[y].show) {
                            f = !1;
                            break
                        }
                    f && (d.lines.show = !0)
                }
                null == d.lines.zero && (d.lines.zero = !!d.lines.fill);
                d.xaxis = L(E, u(d, "x"));
                d.yaxis = L(I, u(d, "y"))
            }
            ka()
        }

        function u(a, c) {
            var b = a[c + "axis"];
            "object" == typeof b && (b = b.n);
            "number" != typeof b && (b = 1);
            return b
        }

        function F() {
            return m.grep(E.concat(I), function (a) {
                return a
            })
        }

        function W(a) {
            var c = {},
                b, d;
            for (b = 0; b < E.length; ++b)(d = E[b]) && d.used && (c["x" + d.n] = d.c2p(a.left));
            for (b = 0; b < I.length; ++b)(d = I[b]) && d.used && (c["y" + d.n] = d.c2p(a.top));
            void 0 !== c.x1 &&
            (c.x = c.x1);
            void 0 !== c.y1 && (c.y = c.y1);
            return c
        }

        function L(a, c) {
            a[c - 1] || (a[c - 1] = {
                n: c,
                direction: a == E ? "x" : "y",
                options: m.extend(!0, {}, a == E ? e.xaxis : e.yaxis)
            });
            return a[c - 1]
        }

        function ka() {
            function a(a, b, c) {
                b < a.datamin && b != -d && (a.datamin = b);
                c > a.datamax && c != d && (a.datamax = c)
            }

            var c = Number.POSITIVE_INFINITY,
                b = Number.NEGATIVE_INFINITY,
                d = Number.MAX_VALUE,
                f, q, t, y, r, e, l, g, k, n, h, D;
            m.each(F(), function (a, d) {
                d.datamin = c;
                d.datamax = b;
                d.used = !1
            });
            for (f = 0; f < w.length; ++f) r = w[f], r.datapoints = {
                points: []
            }, s(G.processRawData, [r, r.data, r.datapoints]);
            for (f = 0; f < w.length; ++f) {
                r = w[f];
                h = r.data;
                D = r.datapoints.format;
                if (!D) {
                    D = [];
                    D.push({
                        x: !0,
                        number: !0,
                        required: !0
                    });
                    D.push({
                        y: !0,
                        number: !0,
                        required: !0
                    });
                    if (r.bars.show || r.lines.show && r.lines.fill) D.push({
                        y: !0,
                        number: !0,
                        required: !1,
                        defaultValue: 0,
                        autoscale: !!(r.bars.show && r.bars.zero || r.lines.show && r.lines.zero)
                    }), r.bars.horizontal && (delete D[D.length - 1].y, D[D.length - 1].x = !0);
                    r.datapoints.format = D
                }
                if (null == r.datapoints.pointsize) {
                    r.datapoints.pointsize = D.length;
                    l = r.datapoints.pointsize;
                    e = r.datapoints.points;
                    var v = r.lines.show && r.lines.steps;
                    r.xaxis.used = r.yaxis.used = !0;
                    for (q = t = 0; q < h.length; ++q, t += l) {
                        n = h[q];
                        var T = null == n;
                        if (!T)
                            for (y = 0; y < l; ++y) {
                                g = n[y];
                                if (k = D[y]) k.number && null != g && (g = +g, isNaN(g) ? g = null : Infinity == g ? g = d : -Infinity == g && (g = -d)), null == g && (k.required && (T = !0), null != k.defaultValue && (g = k.defaultValue));
                                e[t + y] = g
                            }
                        if (T)
                            for (y = 0; y < l; ++y) g = e[t + y], null != g && (k = D[y], !1 !== k.autoscale && (k.x && a(r.xaxis, g, g), k.y && a(r.yaxis, g, g))), e[t + y] = null;
                        else if (v && 0 < t && null != e[t - l] && e[t - l] != e[t] && e[t -
                            l + 1] != e[t + 1]) {
                            for (y = 0; y < l; ++y) e[t + l + y] = e[t + y];
                            e[t + 1] = e[t - l + 1];
                            t += l
                        }
                    }
                }
            }
            for (f = 0; f < w.length; ++f) r = w[f], s(G.processDatapoints, [r, r.datapoints]);
            for (f = 0; f < w.length; ++f) {
                r = w[f];
                e = r.datapoints.points;
                l = r.datapoints.pointsize;
                D = r.datapoints.format;
                n = t = c;
                v = h = b;
                for (q = 0; q < e.length; q += l)
                    if (null != e[q])
                        for (y = 0; y < l; ++y) g = e[q + y], (k = D[y]) && !1 !== k.autoscale && g != d && g != -d && (k.x && (g < t && (t = g), g > h && (h = g)), k.y && (g < n && (n = g), g > v && (v = g)));
                if (r.bars.show) {
                    switch (r.bars.align) {
                        case "left":
                            q = 0;
                            break;
                        case "right":
                            q = -r.bars.barWidth;
                            break;
                        default:
                            q = -r.bars.barWidth / 2
                    }
                    r.bars.horizontal ? (n += q, v += q + r.bars.barWidth) : (t += q, h += q + r.bars.barWidth)
                }
                a(r.xaxis, t, h);
                a(r.yaxis, n, v)
            }
            m.each(F(), function (a, d) {
                d.datamin == c && (d.datamin = null);
                d.datamax == b && (d.datamax = null)
            })
        }

        function X() {
            R && clearTimeout(R);
            M.unbind("mousemove", Y);
            M.unbind("mouseleave", Z);
            M.unbind("click", $);
            s(G.shutdown, [M])
        }

        function la(a) {
            function c(a) {
                return a
            }

            var b, d, f = a.options.transform || c,
                q = a.options.inverseTransform;
            "x" == a.direction ? (b = a.scale = N / Math.abs(f(a.max) - f(a.min)),
                d = Math.min(f(a.max), f(a.min))) : (b = a.scale = J / Math.abs(f(a.max) - f(a.min)), b = -b, d = Math.max(f(a.max), f(a.min)));
            a.p2c = f == c ? function (a) {
                return (a - d) * b
            } : function (a) {
                return (f(a) - d) * b
            };
            a.c2p = q ? function (a) {
                return q(d + a / b)
            } : function (a) {
                return d + a / b
            }
        }

        function ma(a) {
            var c = a.labelWidth,
                b = a.labelHeight,
                d = a.options.position,
                f = "x" === a.direction,
                q = a.options.tickLength,
                t = e.grid.axisMargin,
                y = e.grid.labelMargin,
                r = !0,
                g = !0,
                l = !0,
                k = !1;
            m.each(f ? E : I, function (b, c) {
                c && (c.show || c.reserveSpace) && (c === a ? k = !0 : c.options.position ===
                    d && (k ? g = !1 : r = !1), k || (l = !1))
            });
            g && (t = 0);
            null == q && (q = l ? "full" : 5);
            isNaN(+q) || (y += +q);
            f ? (b += y, "bottom" == d ? (n.bottom += b + t, a.box = {
                top: B.height - n.bottom,
                height: b
            }) : (a.box = {
                top: n.top + t,
                height: b
            }, n.top += b + t)) : (c += y, "left" == d ? (a.box = {
                left: n.left + t,
                width: c
            }, n.left += c + t) : (n.right += c + t, a.box = {
                left: B.width - n.right,
                width: c
            }));
            a.position = d;
            a.tickLength = q;
            a.box.padding = y;
            a.innermost = r
        }

        function na() {
            var a = e.grid.minBorderMargin,
                c;
            if (null == a)
                for (c = a = 0; c < w.length; ++c) a = Math.max(a, 2 * (w[c].points.radius + w[c].points.lineWidth /
                    2));
            var b = a,
                d = a,
                f = a,
                q = a;
            m.each(F(), function (a, c) {
                c.reserveSpace && c.ticks && c.ticks.length && ("x" === c.direction ? (b = Math.max(b, c.labelWidth / 2), d = Math.max(d, c.labelWidth / 2)) : (q = Math.max(q, c.labelHeight / 2), f = Math.max(f, c.labelHeight / 2)))
            });
            n.left = Math.ceil(Math.max(b, n.left));
            n.right = Math.ceil(Math.max(d, n.right));
            n.top = Math.ceil(Math.max(f, n.top));
            n.bottom = Math.ceil(Math.max(q, n.bottom))
        }

        function aa() {
            var a, c = F(),
                b = e.grid.show;
            for (a in n) {
                var d = e.grid.margin || 0;
                n[a] = "number" == typeof d ? d : d[a] || 0
            }
            s(G.processOffset, [n]);
            for (a in n) n[a] = "object" == typeof e.grid.borderWidth ? n[a] + (b ? e.grid.borderWidth[a] : 0) : n[a] + (b ? e.grid.borderWidth : 0);
            m.each(c, function (a, b) {
                var c = b.options;
                b.show = null == c.show ? b.used : c.show;
                b.reserveSpace = null == c.reserveSpace ? b.show : c.reserveSpace;
                var c = b.options,
                    d = +(null != c.min ? c.min : b.datamin),
                    r = +(null != c.max ? c.max : b.datamax),
                    e = r - d;
                if (0 == e) {
                    if (e = 0 == r ? 1 : .01, null == c.min && (d -= e), null == c.max || null != c.min) r += e
                } else {
                    var g = c.autoscaleMargin;
                    null != g && (null == c.min && (d -= e * g, 0 > d && null != b.datamin && 0 <= b.datamin &&
                    (d = 0)), null == c.max && (r += e * g, 0 < r && null != b.datamax && 0 >= b.datamax && (r = 0)))
                }
                b.min = d;
                b.max = r
            });
            if (b) {
                d = m.grep(c, function (a) {
                    return a.show || a.reserveSpace
                });
                m.each(d, function (a, b) {
                    oa(b);
                    var c = b.options.ticks,
                        d = [];
                    null == c || "number" == typeof c && 0 < c ? d = b.tickGenerator(b) : c && (d = m.isFunction(c) ? c(b) : c);
                    var r;
                    b.ticks = [];
                    for (c = 0; c < d.length; ++c) {
                        var e = null,
                            g = d[c];
                        "object" == typeof g ? (r = +g[0], 1 < g.length && (e = g[1])) : r = +g;
                        null == e && (e = b.tickFormatter(r, b));
                        isNaN(r) || b.ticks.push({
                            v: r,
                            label: e
                        })
                    }
                    d = b.ticks;
                    b.options.autoscaleMargin &&
                    0 < d.length && (null == b.options.min && (b.min = Math.min(b.min, d[0].v)), null == b.options.max && 1 < d.length && (b.max = Math.max(b.max, d[d.length - 1].v)));
                    d = b.options;
                    c = b.ticks || [];
                    r = d.labelWidth || 0;
                    for (var e = d.labelHeight || 0, g = r || ("x" == b.direction ? Math.floor(B.width / (c.length || 1)) : null), l = "flot-" + b.direction + "-axis flot-" + b.direction + b.n + "-axis " + (b.direction + "Axis " + b.direction + b.n + "Axis"), k = d.font || "flot-tick-label tickLabel", n = 0; n < c.length; ++n) {
                        var h = c[n];
                        h.label && (h = B.getTextInfo(l, h.label, k, null, g), r = Math.max(r,
                            h.width), e = Math.max(e, h.height))
                    }
                    b.labelWidth = d.labelWidth || r;
                    b.labelHeight = d.labelHeight || e
                });
                for (a = d.length - 1; 0 <= a; --a) ma(d[a]);
                na();
                m.each(d, function (a, b) {
                    "x" == b.direction ? (b.box.left = n.left - b.labelWidth / 2, b.box.width = B.width - n.left - n.right + b.labelWidth) : (b.box.top = n.top - b.labelHeight / 2, b.box.height = B.height - n.bottom - n.top + b.labelHeight)
                })
            }
            N = B.width - n.left - n.right;
            J = B.height - n.bottom - n.top;
            m.each(c, function (a, b) {
                la(b)
            });
            b && pa();
            qa()
        }

        function oa(a) {
            var c = a.options,
                b;
            b = "number" == typeof c.ticks &&
            0 < c.ticks ? c.ticks : .3 * Math.sqrt("x" == a.direction ? B.width : B.height);
            b = (a.max - a.min) / b;
            var d = -Math.floor(Math.log(b) / Math.LN10),
                f = c.tickDecimals;
            null != f && d > f && (d = f);
            var e = Math.pow(10, -d),
                t = b / e,
                g;
            1.5 > t ? g = 1 : 3 > t ? (g = 2, 2.25 < t && (null == f || d + 1 <= f) && (g = 2.5, ++d)) : g = 7.5 > t ? 5 : 10;
            g *= e;
            null != c.minTickSize && g < c.minTickSize && (g = c.minTickSize);
            a.delta = b;
            a.tickDecimals = Math.max(0, null != f ? f : d);
            a.tickSize = c.tickSize || g;
            if ("time" == c.mode && !a.tickGenerator) throw Error("Time mode requires the flot.time plugin.");
            a.tickGenerator ||
            (a.tickGenerator = function (a) {
                var b = [],
                    c;
                c = a.tickSize;
                c *= Math.floor(a.min / c);
                var d = 0,
                    f = Number.NaN,
                    e;
                do e = f, f = c + d * a.tickSize, b.push(f), ++d; while (f < a.max && f != e);
                return b
            }, a.tickFormatter = function (a, b) {
                var c = b.tickDecimals ? Math.pow(10, b.tickDecimals) : 1,
                    d = "" + Math.round(a * c) / c;
                if (null != b.tickDecimals) {
                    var f = d.indexOf("."),
                        f = -1 == f ? 0 : d.length - f - 1;
                    if (f < b.tickDecimals) return (f ? d : d + ".") + ("" + c).substr(1, b.tickDecimals - f)
                }
                return d
            });
            m.isFunction(c.tickFormatter) && (a.tickFormatter = function (a, b) {
                return "" + c.tickFormatter(a,
                        b)
            });
            if (null != c.alignTicksWithAxis) {
                var r = ("x" == a.direction ? E : I)[c.alignTicksWithAxis - 1];
                r && r.used && r != a && (b = a.tickGenerator(a), 0 < b.length && (null == c.min && (a.min = Math.min(a.min, b[0])), null == c.max && 1 < b.length && (a.max = Math.max(a.max, b[b.length - 1]))), a.tickGenerator = function (a) {
                    var b = [],
                        c, d;
                    for (d = 0; d < r.ticks.length; ++d) c = (r.ticks[d].v - r.min) / (r.max - r.min), c = a.min + c * (a.max - a.min), b.push(c);
                    return b
                }, a.mode || null != c.tickDecimals || (b = Math.max(0, -Math.floor(Math.log(a.delta) / Math.LN10) + 1), d = a.tickGenerator(a),
                1 < d.length && /\..*0$/.test((d[1] - d[0]).toFixed(b)) || (a.tickDecimals = b)))
            }
        }

        function ba() {
            B.clear();
            s(G.drawBackground, [l]);
            var a = e.grid;
            a.show && a.backgroundColor && (l.save(), l.translate(n.left, n.top), l.fillStyle = ca(e.grid.backgroundColor, J, 0, "rgba(255, 255, 255, 0)"), l.fillRect(0, 0, N, J), l.restore());
            a.show && !a.aboveData && da();
            for (var c = 0; c < w.length; ++c) {
                s(G.drawSeries, [l, w[c]]);
                var b = w[c];
                b.lines.show && ra(b);
                b.bars.show && sa(b);
                b.points.show && ta(b)
            }
            s(G.draw, [l]);
            a.show && a.aboveData && da();
            B.render();
            S()
        }

        function ea(a, c) {
            for (var b, d, f, e, g = F(), l = 0; l < g.length; ++l)
                if (b = g[l], b.direction == c && (e = c + b.n + "axis", a[e] || 1 != b.n || (e = c + "axis"), a[e])) {
                    d = a[e].from;
                    f = a[e].to;
                    break
                }
            a[e] || (b = "x" == c ? E[0] : I[0], d = a[c + "1"], f = a[c + "2"]);
            null != d && null != f && d > f && (e = d, d = f, f = e);
            return {
                from: d,
                to: f,
                axis: b
            }
        }

        function da() {
            var a, c, b;
            l.save();
            l.translate(n.left, n.top);
            if (b = e.grid.markings)
                for (m.isFunction(b) && (c = x.getAxes(), c.xmin = c.xaxis.min, c.xmax = c.xaxis.max, c.ymin = c.yaxis.min, c.ymax = c.yaxis.max, b = b(c)), a = 0; a < b.length; ++a) {
                    c = b[a];
                    var d = ea(c, "x"),
                        f = ea(c, "y");
                    null == d.from && (d.from = d.axis.min);
                    null == d.to && (d.to = d.axis.max);
                    null == f.from && (f.from = f.axis.min);
                    null == f.to && (f.to = f.axis.max);
                    if (!(d.to < d.axis.min || d.from > d.axis.max || f.to < f.axis.min || f.from > f.axis.max)) {
                        d.from = Math.max(d.from, d.axis.min);
                        d.to = Math.min(d.to, d.axis.max);
                        f.from = Math.max(f.from, f.axis.min);
                        f.to = Math.min(f.to, f.axis.max);
                        var g = d.from === d.to,
                            t = f.from === f.to;
                        if (!g || !t)
                            if (d.from = Math.floor(d.axis.p2c(d.from)), d.to = Math.floor(d.axis.p2c(d.to)), f.from = Math.floor(f.axis.p2c(f.from)),
                                    f.to = Math.floor(f.axis.p2c(f.to)), g || t) {
                                var t = c.lineWidth || e.grid.markingsLineWidth,
                                    k = t % 2 ? .5 : 0;
                                l.beginPath();
                                l.strokeStyle = c.color || e.grid.markingsColor;
                                l.lineWidth = t;
                                g ? (l.moveTo(d.to + k, f.from), l.lineTo(d.to + k, f.to)) : (l.moveTo(d.from, f.to + k), l.lineTo(d.to, f.to + k));
                                l.stroke()
                            } else l.fillStyle = c.color || e.grid.markingsColor, l.fillRect(d.from, f.to, d.to - d.from, f.from - f.to)
                    }
                }
            c = F();
            b = e.grid.borderWidth;
            for (d = 0; d < c.length; ++d) {
                f = c[d];
                a = f.box;
                var g = f.tickLength,
                    r, P;
                if (f.show && 0 != f.ticks.length) {
                    l.lineWidth =
                        1;
                    "x" == f.direction ? (t = 0, k = "full" == g ? "top" == f.position ? 0 : J : a.top - n.top + ("top" == f.position ? a.height : 0)) : (k = 0, t = "full" == g ? "left" == f.position ? 0 : N : a.left - n.left + ("left" == f.position ? a.width : 0));
                    f.innermost || (l.strokeStyle = f.options.color, l.beginPath(), r = P = 0, "x" == f.direction ? r = N + 1 : P = J + 1, 1 == l.lineWidth && ("x" == f.direction ? k = Math.floor(k) + .5 : t = Math.floor(t) + .5), l.moveTo(t, k), l.lineTo(t + r, k + P), l.stroke());
                    l.strokeStyle = f.options.tickColor;
                    l.beginPath();
                    for (a = 0; a < f.ticks.length; ++a) {
                        var h = f.ticks[a].v;
                        r = P = 0;
                        isNaN(h) || h < f.min || h > f.max || "full" == g && ("object" == typeof b && 0 < b[f.position] || 0 < b) && (h == f.min || h == f.max) || ("x" == f.direction ? (t = f.p2c(h), P = "full" == g ? -J : g, "top" == f.position && (P = -P)) : (k = f.p2c(h), r = "full" == g ? -N : g, "left" == f.position && (r = -r)), 1 == l.lineWidth && ("x" == f.direction ? t = Math.floor(t) + .5 : k = Math.floor(k) + .5), l.moveTo(t, k), l.lineTo(t + r, k + P))
                    }
                    l.stroke()
                }
            }
            b && (a = e.grid.borderColor, "object" == typeof b || "object" == typeof a ? ("object" !== typeof b && (b = {
                top: b,
                right: b,
                bottom: b,
                left: b
            }), "object" !== typeof a && (a = {
                top: a,
                right: a,
                bottom: a,
                left: a
            }), 0 < b.top && (l.strokeStyle = a.top, l.lineWidth = b.top, l.beginPath(), l.moveTo(0 - b.left, 0 - b.top / 2), l.lineTo(N, 0 - b.top / 2), l.stroke()), 0 < b.right && (l.strokeStyle = a.right, l.lineWidth = b.right, l.beginPath(), l.moveTo(N + b.right / 2, 0 - b.top), l.lineTo(N + b.right / 2, J), l.stroke()), 0 < b.bottom && (l.strokeStyle = a.bottom, l.lineWidth = b.bottom, l.beginPath(), l.moveTo(N + b.right, J + b.bottom / 2), l.lineTo(0, J + b.bottom / 2), l.stroke()), 0 < b.left && (l.strokeStyle = a.left, l.lineWidth = b.left, l.beginPath(), l.moveTo(0 -
                b.left / 2, J + b.bottom), l.lineTo(0 - b.left / 2, 0), l.stroke())) : (l.lineWidth = b, l.strokeStyle = e.grid.borderColor, l.strokeRect(-b / 2, -b / 2, N + b, J + b)));
            l.restore()
        }

        function pa() {
            m.each(F(), function (a, c) {
                var b = c.box,
                    d = "flot-" + c.direction + "-axis flot-" + c.direction + c.n + "-axis " + (c.direction + "Axis " + c.direction + c.n + "Axis"),
                    f = c.options.font || "flot-tick-label tickLabel",
                    e, g, l, r, k;
                B.removeText(d);
                if (c.show && 0 != c.ticks.length)
                    for (var h = 0; h < c.ticks.length; ++h) e = c.ticks[h], !e.label || e.v < c.min || e.v > c.max || ("x" == c.direction ?
                        (r = "center", g = n.left + c.p2c(e.v), "bottom" == c.position ? l = b.top + b.padding : (l = b.top + b.height - b.padding, k = "bottom")) : (k = "middle", l = n.top + c.p2c(e.v), "left" == c.position ? (g = b.left + b.width - b.padding, r = "right") : g = b.left + b.padding), B.addText(d, g, l, e.label, f, null, null, r, k))
            })
        }

        function ra(a) {
            function c(a, b, c, d, f) {
                var e = a.points;
                a = a.pointsize;
                var g = null,
                    k = null;
                l.beginPath();
                for (var h = a; h < e.length; h += a) {
                    var n = e[h - a],
                        v = e[h - a + 1],
                        m = e[h],
                        q = e[h + 1];
                    if (null != n && null != m) {
                        if (v <= q && v < f.min) {
                            if (q < f.min) continue;
                            n = (f.min - v) /
                                (q - v) * (m - n) + n;
                            v = f.min
                        } else if (q <= v && q < f.min) {
                            if (v < f.min) continue;
                            m = (f.min - v) / (q - v) * (m - n) + n;
                            q = f.min
                        }
                        if (v >= q && v > f.max) {
                            if (q > f.max) continue;
                            n = (f.max - v) / (q - v) * (m - n) + n;
                            v = f.max
                        } else if (q >= v && q > f.max) {
                            if (v > f.max) continue;
                            m = (f.max - v) / (q - v) * (m - n) + n;
                            q = f.max
                        }
                        if (n <= m && n < d.min) {
                            if (m < d.min) continue;
                            v = (d.min - n) / (m - n) * (q - v) + v;
                            n = d.min
                        } else if (m <= n && m < d.min) {
                            if (n < d.min) continue;
                            q = (d.min - n) / (m - n) * (q - v) + v;
                            m = d.min
                        }
                        if (n >= m && n > d.max) {
                            if (m > d.max) continue;
                            v = (d.max - n) / (m - n) * (q - v) + v;
                            n = d.max
                        } else if (m >= n && m > d.max) {
                            if (n > d.max) continue;
                            q = (d.max - n) / (m - n) * (q - v) + v;
                            m = d.max
                        }
                        n == g && v == k || l.moveTo(d.p2c(n) + b, f.p2c(v) + c);
                        g = m;
                        k = q;
                        l.lineTo(d.p2c(m) + b, f.p2c(q) + c)
                    }
                }
                l.stroke()
            }

            function b(a, b, c) {
                var d = a.points;
                a = a.pointsize;
                for (var f = Math.min(Math.max(0, c.min), c.max), e = 0, g = !1, k = 1, n = 0, m = 0; !(0 < a && e > d.length + a);) {
                    var e = e + a,
                        h = d[e - a],
                        q = d[e - a + k],
                        p = d[e],
                        s = d[e + k];
                    if (g) {
                        if (0 < a && null != h && null == p) {
                            m = e;
                            a = -a;
                            k = 2;
                            continue
                        }
                        if (0 > a && e == n + a) {
                            l.fill();
                            g = !1;
                            a = -a;
                            k = 1;
                            e = n = m + a;
                            continue
                        }
                    }
                    if (null != h && null != p) {
                        if (h <= p && h < b.min) {
                            if (p < b.min) continue;
                            q = (b.min - h) / (p - h) * (s -
                                q) + q;
                            h = b.min
                        } else if (p <= h && p < b.min) {
                            if (h < b.min) continue;
                            s = (b.min - h) / (p - h) * (s - q) + q;
                            p = b.min
                        }
                        if (h >= p && h > b.max) {
                            if (p > b.max) continue;
                            q = (b.max - h) / (p - h) * (s - q) + q;
                            h = b.max
                        } else if (p >= h && p > b.max) {
                            if (h > b.max) continue;
                            s = (b.max - h) / (p - h) * (s - q) + q;
                            p = b.max
                        }
                        g || (l.beginPath(), l.moveTo(b.p2c(h), c.p2c(f)), g = !0);
                        if (q >= c.max && s >= c.max) l.lineTo(b.p2c(h), c.p2c(c.max)), l.lineTo(b.p2c(p), c.p2c(c.max));
                        else if (q <= c.min && s <= c.min) l.lineTo(b.p2c(h), c.p2c(c.min)), l.lineTo(b.p2c(p), c.p2c(c.min));
                        else {
                            var w = h,
                                x = p;
                            q <= s && q < c.min && s >=
                            c.min ? (h = (c.min - q) / (s - q) * (p - h) + h, q = c.min) : s <= q && s < c.min && q >= c.min && (p = (c.min - q) / (s - q) * (p - h) + h, s = c.min);
                            q >= s && q > c.max && s <= c.max ? (h = (c.max - q) / (s - q) * (p - h) + h, q = c.max) : s >= q && s > c.max && q <= c.max && (p = (c.max - q) / (s - q) * (p - h) + h, s = c.max);
                            h != w && l.lineTo(b.p2c(w), c.p2c(q));
                            l.lineTo(b.p2c(h), c.p2c(q));
                            l.lineTo(b.p2c(p), c.p2c(s));
                            p != x && (l.lineTo(b.p2c(p), c.p2c(s)), l.lineTo(b.p2c(x), c.p2c(s)))
                        }
                    }
                }
            }

            l.save();
            l.translate(n.left, n.top);
            l.lineJoin = "round";
            var d = a.lines.lineWidth,
                f = a.shadowSize;
            if (0 < d && 0 < f) {
                l.lineWidth = f;
                l.strokeStyle = "rgba(0,0,0,0.1)";
                var e = Math.PI / 18;
                c(a.datapoints, Math.sin(e) * (d / 2 + f / 2), Math.cos(e) * (d / 2 + f / 2), a.xaxis, a.yaxis);
                l.lineWidth = f / 2;
                c(a.datapoints, Math.sin(e) * (d / 2 + f / 4), Math.cos(e) * (d / 2 + f / 4), a.xaxis, a.yaxis)
            }
            l.lineWidth = d;
            l.strokeStyle = a.color;
            if (f = U(a.lines, a.color, 0, J)) l.fillStyle = f, b(a.datapoints, a.xaxis, a.yaxis);
            0 < d && c(a.datapoints, 0, 0, a.xaxis, a.yaxis);
            l.restore()
        }

        function ta(a) {
            function c(a, b, c, d, f, e, g, k) {
                var h = a.points;
                a = a.pointsize;
                for (var n = 0; n < h.length; n += a) {
                    var q = h[n],
                        m = h[n + 1];
                    null == q || q < e.min || q > e.max || m < g.min || m > g.max || (l.beginPath(), q = e.p2c(q), m = g.p2c(m) + d, "circle" == k ? l.arc(q, m, b, 0, f ? Math.PI : 2 * Math.PI, !1) : k(l, q, m, b, f), l.closePath(), c && (l.fillStyle = c, l.fill()), l.stroke())
                }
            }

            l.save();
            l.translate(n.left, n.top);
            var b = a.points.lineWidth,
                d = a.shadowSize,
                f = a.points.radius,
                e = a.points.symbol;
            0 == b && (b = 1E-4);
            0 < b && 0 < d && (d /= 2, l.lineWidth = d, l.strokeStyle = "rgba(0,0,0,0.1)", c(a.datapoints, f, null, d + d / 2, !0, a.xaxis, a.yaxis, e), l.strokeStyle = "rgba(0,0,0,0.2)", c(a.datapoints, f, null, d / 2, !0,
                a.xaxis, a.yaxis, e));
            l.lineWidth = b;
            l.strokeStyle = a.color;
            c(a.datapoints, f, U(a.points, a.color), 0, !1, a.xaxis, a.yaxis, e);
            l.restore()
        }

        function fa(a, c, b, d, f, e, g, k, l, h, n) {
            var m, p, s, w;
            h ? (w = p = s = !0, m = !1, h = b, b = c + d, f = c + f, a < h && (c = a, a = h, h = c, m = !0, p = !1)) : (m = p = s = !0, w = !1, h = a + d, a += f, f = b, b = c, b < f && (c = b, b = f, f = c, w = !0, s = !1));
            a < g.min || h > g.max || b < k.min || f > k.max || (h < g.min && (h = g.min, m = !1), a > g.max && (a = g.max, p = !1), f < k.min && (f = k.min, w = !1), b > k.max && (b = k.max, s = !1), h = g.p2c(h), f = k.p2c(f), a = g.p2c(a), b = k.p2c(b), e && (l.fillStyle = e(f, b),
                l.fillRect(h, b, a - h, f - b)), 0 < n && (m || p || s || w) && (l.beginPath(), l.moveTo(h, f), m ? l.lineTo(h, b) : l.moveTo(h, b), s ? l.lineTo(a, b) : l.moveTo(a, b), p ? l.lineTo(a, f) : l.moveTo(a, f), w ? l.lineTo(h, f) : l.moveTo(h, f), l.stroke()))
        }

        function sa(a) {
            l.save();
            l.translate(n.left, n.top);
            l.lineWidth = a.bars.lineWidth;
            l.strokeStyle = a.color;
            var c;
            switch (a.bars.align) {
                case "left":
                    c = 0;
                    break;
                case "right":
                    c = -a.bars.barWidth;
                    break;
                default:
                    c = -a.bars.barWidth / 2
            }
            (function (b, c, f, e, g, h) {
                var k = b.points;
                b = b.pointsize;
                for (var n = 0; n < k.length; n +=
                    b) null != k[n] && fa(k[n], k[n + 1], k[n + 2], c, f, e, g, h, l, a.bars.horizontal, a.bars.lineWidth)
            })(a.datapoints, c, c + a.bars.barWidth, a.bars.fill ? function (b, c) {
                return U(a.bars, a.color, b, c)
            } : null, a.xaxis, a.yaxis);
            l.restore()
        }

        function U(a, c, b, d) {
            var f = a.fill;
            if (!f) return null;
            if (a.fillColor) return ca(a.fillColor, b, d, c);
            a = m.color.parse(c);
            a.a = "number" == typeof f ? f : .4;
            a.normalize();
            return a.toString()
        }

        function qa() {
            null != e.legend.container ? m(e.legend.container).html("") : g.find(".legend").remove();
            if (e.legend.show) {
                for (var a = [], c = [], b = !1, d = e.legend.labelFormatter, f, k, h = 0; h < w.length; ++h) f = w[h], f.label && (k = d ? d(f.label, f) : f.label) && c.push({
                    label: k,
                    color: f.color
                });
                if (e.legend.sorted)
                    if (m.isFunction(e.legend.sorted)) c.sort(e.legend.sorted);
                    else if ("reverse" == e.legend.sorted) c.reverse();
                    else {
                        var l = "descending" != e.legend.sorted;
                        c.sort(function (a, b) {
                            return a.label == b.label ? 0 : a.label < b.label != l ? 1 : -1
                        })
                    }
                for (h = 0; h < c.length; ++h) d = c[h], 0 == h % e.legend.noColumns && (b && a.push("</tr>"), a.push("<tr>"), b = !0), a.push('<td class="legendColorBox"><div style="border:1px solid ' +
                    e.legend.labelBoxBorderColor + ';padding:1px"><div style="width:4px;height:0;border:5px solid ' + d.color + ';overflow:hidden"></div></div></td><td class="legendLabel">' + d.label + "</td>");
                b && a.push("</tr>");
                0 != a.length && (c = '<table style="font-size:smaller;color:' + e.grid.color + '">' + a.join("") + "</table>", null != e.legend.container ? m(e.legend.container).html(c) : (a = "", b = e.legend.position, h = e.legend.margin, null == h[0] && (h = [h, h]), "n" == b.charAt(0) ? a += "top:" + (h[1] + n.top) + "px;" : "s" == b.charAt(0) && (a += "bottom:" + (h[1] +
                        n.bottom) + "px;"), "e" == b.charAt(1) ? a += "right:" + (h[0] + n.right) + "px;" : "w" == b.charAt(1) && (a += "left:" + (h[0] + n.left) + "px;"), c = m('<div class="legend">' + c.replace('style="', 'style="position:absolute;' + a + ";") + "</div>").appendTo(g), 0 != e.legend.backgroundOpacity && (b = e.legend.backgroundColor, null == b && (b = (b = e.grid.backgroundColor) && "string" == typeof b ? m.color.parse(b) : m.color.extract(c, "background-color"), b.a = 1, b = b.toString()), h = c.children(), m('<div style="position:absolute;width:' + h.width() + "px;height:" + h.height() +
                    "px;" + a + "background-color:" + b + ';"> </div>').prependTo(c).css("opacity", e.legend.backgroundOpacity))))
            }
        }

        function Y(a) {
            e.grid.hoverable && V("plothover", a, function (a) {
                return !1 != a.hoverable
            })
        }

        function Z(a) {
            e.grid.hoverable && V("plothover", a, function (a) {
                return !1
            })
        }

        function $(a) {
            V("plotclick", a, function (a) {
                return !1 != a.clickable
            })
        }

        function V(a, c, b) {
            var d = M.offset(),
                f = c.pageX - d.left - n.left,
                h = c.pageY - d.top - n.top,
                k = W({
                    left: f,
                    top: h
                });
            k.pageX = c.pageX;
            k.pageY = c.pageY;
            c = e.grid.mouseActiveRadius;
            var l = c * c + 1,
                m = null,
                p, s, x;
            for (p = w.length - 1; 0 <= p; --p)
                if (b(w[p])) {
                    var H = w[p],
                        u = H.xaxis,
                        K = H.yaxis,
                        D = H.datapoints.points,
                        v = u.c2p(f),
                        B = K.c2p(h),
                        F = c / u.scale,
                        E = c / K.scale;
                    x = H.datapoints.pointsize;
                    u.options.inverseTransform && (F = Number.MAX_VALUE);
                    K.options.inverseTransform && (E = Number.MAX_VALUE);
                    if (H.lines.show || H.points.show)
                        for (s = 0; s < D.length; s += x) {
                            var A = D[s],
                                z = D[s + 1];
                            null == A || A - v > F || A - v < -F || z - B > E || z - B < -E || (A = Math.abs(u.p2c(A) - f), z = Math.abs(K.p2c(z) - h), z = A * A + z * z, z < l && (l = z, m = [p, s / x]))
                        }
                    if (H.bars.show && !m) {
                        switch (H.bars.align) {
                            case "left":
                                u =
                                    0;
                                break;
                            case "right":
                                u = -H.bars.barWidth;
                                break;
                            default:
                                u = -H.bars.barWidth / 2
                        }
                        H = u + H.bars.barWidth;
                        for (s = 0; s < D.length; s += x) A = D[s], z = D[s + 1], K = D[s + 2], null != A && (w[p].bars.horizontal ? v <= Math.max(K, A) && v >= Math.min(K, A) && B >= z + u && B <= z + H : v >= A + u && v <= A + H && B >= Math.min(K, z) && B <= Math.max(K, z)) && (m = [p, s / x])
                    }
                }
            m ? (p = m[0], s = m[1], x = w[p].datapoints.pointsize, b = {
                datapoint: w[p].datapoints.points.slice(s * x, (s + 1) * x),
                dataIndex: s,
                series: w[p],
                seriesIndex: p
            }) : b = null;
            b && (b.pageX = parseInt(b.series.xaxis.p2c(b.datapoint[0]) + d.left +
                n.left, 10), b.pageY = parseInt(b.series.yaxis.p2c(b.datapoint[1]) + d.top + n.top, 10));
            if (e.grid.autoHighlight) {
                for (d = 0; d < O.length; ++d) f = O[d], f.auto != a || b && f.series == b.series && f.point[0] == b.datapoint[0] && f.point[1] == b.datapoint[1] || ga(f.series, f.point);
                b && ha(b.series, b.datapoint, a)
            }
            g.trigger(a, [k, b])
        }

        function S() {
            var a = e.interaction.redrawOverlayInterval;
            -1 == a ? ia() : R || (R = setTimeout(ia, a))
        }

        function ia() {
            R = null;
            A.save();
            Q.clear();
            A.translate(n.left, n.top);
            var a, c;
            for (a = 0; a < O.length; ++a)
                if (c = O[a], c.series.bars.show) ua(c.series,
                    c.point);
                else {
                    var b = c.series,
                        d = c.point;
                    c = d[0];
                    var d = d[1],
                        f = b.xaxis,
                        e = b.yaxis,
                        g = "string" === typeof b.highlightColor ? b.highlightColor : m.color.parse(b.color).scale("a", .5).toString();
                    if (!(c < f.min || c > f.max || d < e.min || d > e.max)) {
                        var h = b.points.radius + b.points.lineWidth / 2;
                        A.lineWidth = h;
                        A.strokeStyle = g;
                        g = 1.5 * h;
                        c = f.p2c(c);
                        d = e.p2c(d);
                        A.beginPath();
                        "circle" == b.points.symbol ? A.arc(c, d, g, 0, 2 * Math.PI, !1) : b.points.symbol(A, c, d, g, !1);
                        A.closePath();
                        A.stroke()
                    }
                }
            A.restore();
            s(G.drawOverlay, [A])
        }

        function ha(a, c, b) {
            "number" ==
            typeof a && (a = w[a]);
            if ("number" == typeof c) {
                var d = a.datapoints.pointsize;
                c = a.datapoints.points.slice(d * c, d * (c + 1))
            }
            d = ja(a, c);
            -1 == d ? (O.push({
                series: a,
                point: c,
                auto: b
            }), S()) : b || (O[d].auto = !1)
        }

        function ga(a, c) {
            if (null == a && null == c) O = [], S();
            else {
                "number" == typeof a && (a = w[a]);
                if ("number" == typeof c) {
                    var b = a.datapoints.pointsize;
                    c = a.datapoints.points.slice(b * c, b * (c + 1))
                }
                b = ja(a, c);
                -1 != b && (O.splice(b, 1), S())
            }
        }

        function ja(a, c) {
            for (var b = 0; b < O.length; ++b) {
                var d = O[b];
                if (d.series == a && d.point[0] == c[0] && d.point[1] == c[1]) return b
            }
            return -1
        }

        function ua(a, c) {
            var b = "string" === typeof a.highlightColor ? a.highlightColor : m.color.parse(a.color).scale("a", .5).toString(),
                d;
            switch (a.bars.align) {
                case "left":
                    d = 0;
                    break;
                case "right":
                    d = -a.bars.barWidth;
                    break;
                default:
                    d = -a.bars.barWidth / 2
            }
            A.lineWidth = a.bars.lineWidth;
            A.strokeStyle = b;
            fa(c[0], c[1], c[2] || 0, d, d + a.bars.barWidth, function () {
                return b
            }, a.xaxis, a.yaxis, A, a.bars.horizontal, a.bars.lineWidth)
        }

        function ca(a, c, b, d) {
            if ("string" == typeof a) return a;
            c = l.createLinearGradient(0, b, 0, c);
            b = 0;
            for (var f = a.colors.length; b <
            f; ++b) {
                var e = a.colors[b];
                if ("string" != typeof e) {
                    var g = m.color.parse(d);
                    null != e.brightness && (g = g.scale("rgb", e.brightness));
                    null != e.opacity && (g.a *= e.opacity);
                    e = g.toString()
                }
                c.addColorStop(b / (f - 1), e)
            }
            return c
        }

        var w = [],
            e = {
                colors: ["#edc240", "#afd8f8", "#cb4b4b", "#4da74d", "#9440ed"],
                legend: {
                    show: !0,
                    noColumns: 1,
                    labelFormatter: null,
                    labelBoxBorderColor: "#ccc",
                    container: null,
                    position: "ne",
                    margin: 5,
                    backgroundColor: null,
                    backgroundOpacity: .85,
                    sorted: null
                },
                xaxis: {
                    show: null,
                    position: "bottom",
                    mode: null,
                    font: null,
                    color: null,
                    tickColor: null,
                    transform: null,
                    inverseTransform: null,
                    min: null,
                    max: null,
                    autoscaleMargin: null,
                    ticks: null,
                    tickFormatter: null,
                    labelWidth: null,
                    labelHeight: null,
                    reserveSpace: null,
                    tickLength: null,
                    alignTicksWithAxis: null,
                    tickDecimals: null,
                    tickSize: null,
                    minTickSize: null
                },
                yaxis: {
                    autoscaleMargin: .02,
                    position: "left"
                },
                xaxes: [],
                yaxes: [],
                series: {
                    points: {
                        show: !1,
                        radius: 3,
                        lineWidth: 2,
                        fill: !0,
                        fillColor: "#ffffff",
                        symbol: "circle"
                    },
                    lines: {
                        lineWidth: 2,
                        fill: !1,
                        fillColor: null,
                        steps: !1
                    },
                    bars: {
                        show: !1,
                        lineWidth: 2,
                        barWidth: 1,
                        fill: !0,
                        fillColor: null,
                        align: "left",
                        horizontal: !1,
                        zero: !0
                    },
                    shadowSize: 3,
                    highlightColor: null
                },
                grid: {
                    show: !0,
                    aboveData: !1,
                    color: "#545454",
                    backgroundColor: null,
                    borderColor: null,
                    tickColor: null,
                    margin: 0,
                    labelMargin: 5,
                    axisMargin: 8,
                    borderWidth: 2,
                    minBorderMargin: null,
                    markings: null,
                    markingsColor: "#f4f4f4",
                    markingsLineWidth: 2,
                    clickable: !1,
                    hoverable: !1,
                    autoHighlight: !0,
                    mouseActiveRadius: 10
                },
                interaction: {
                    redrawOverlayInterval: 1E3 / 60
                },
                hooks: {}
            },
            B = null,
            Q = null,
            M = null,
            l = null,
            A = null,
            E = [],
            I = [],
            n = {
                left: 0,
                right: 0,
                top: 0,
                bottom: 0
            },
            N = 0,
            J = 0,
            G = {
                processOptions: [],
                processRawData: [],
                processDatapoints: [],
                processOffset: [],
                drawBackground: [],
                drawSeries: [],
                draw: [],
                bindEvents: [],
                drawOverlay: [],
                shutdown: []
            },
            x = this;
        x.setData = K;
        x.setupGrid = aa;
        x.draw = ba;
        x.getPlaceholder = function () {
            return g
        };
        x.getCanvas = function () {
            return B.element
        };
        x.getPlotOffset = function () {
            return n
        };
        x.width = function () {
            return N
        };
        x.height = function () {
            return J
        };
        x.offset = function () {
            var a = M.offset();
            a.left += n.left;
            a.top += n.top;
            return a
        };
        x.getData = function () {
            return w
        };
        x.getAxes = function () {
            var a = {};
            m.each(E.concat(I), function (c, b) {
                b && (a[b.direction + (1 != b.n ? b.n : "") + "axis"] = b)
            });
            return a
        };
        x.getXAxes = function () {
            return E
        };
        x.getYAxes = function () {
            return I
        };
        x.c2p = W;
        x.p2c = function (a) {
            var c = {},
                b, d, e;
            for (b = 0; b < E.length; ++b)
                if ((d = E[b]) && d.used && (e = "x" + d.n, null == a[e] && 1 == d.n && (e = "x"), null != a[e])) {
                    c.left = d.p2c(a[e]);
                    break
                }
            for (b = 0; b < I.length; ++b)
                if ((d = I[b]) && d.used && (e = "y" + d.n, null == a[e] && 1 == d.n && (e = "y"), null != a[e])) {
                    c.top = d.p2c(a[e]);
                    break
                }
            return c
        };
        x.getOptions = function () {
            return e
        };
        x.highlight = ha;
        x.unhighlight = ga;
        x.triggerRedrawOverlay = S;
        x.pointOffset = function (a) {
            return {
                left: parseInt(E[u(a, "x") - 1].p2c(+a.x) + n.left, 10),
                top: parseInt(I[u(a, "y") - 1].p2c(+a.y) + n.top, 10)
            }
        };
        x.shutdown = X;
        x.destroy = function () {
            X();
            g.removeData("plot").empty();
            w = [];
            A = l = M = Q = B = e = null;
            E = [];
            I = [];
            G = null;
            O = [];
            x = null
        };
        x.resize = function () {
            var a = g.width(),
                c = g.height();
            B.resize(a, c);
            Q.resize(a, c)
        };
        x.hooks = G;
        (function () {
            for (var a = {
                Canvas: C
            }, c = 0; c < p.length; ++c) {
                var b = p[c];
                b.init(x, a);
                b.options && m.extend(!0, e, b.options)
            }
        })(x);
        (function (a) {
            m.extend(!0, e, a);
            a && a.colors && (e.colors = a.colors);
            null == e.xaxis.color && (e.xaxis.color = m.color.parse(e.grid.color).scale("a", .22).toString());
            null == e.yaxis.color && (e.yaxis.color = m.color.parse(e.grid.color).scale("a", .22).toString());
            null == e.xaxis.tickColor && (e.xaxis.tickColor = e.grid.tickColor || e.xaxis.color);
            null == e.yaxis.tickColor && (e.yaxis.tickColor = e.grid.tickColor || e.yaxis.color);
            null == e.grid.borderColor && (e.grid.borderColor = e.grid.color);
            null == e.grid.tickColor && (e.grid.tickColor =
                m.color.parse(e.grid.color).scale("a", .22).toString());
            var c, b;
            a = (a = g.css("font-size")) ? +a.replace("px", "") : 13;
            var d = {
                style: g.css("font-style"),
                size: Math.round(.8 * a),
                variant: g.css("font-variant"),
                weight: g.css("font-weight"),
                family: g.css("font-family")
            };
            b = e.xaxes.length || 1;
            for (a = 0; a < b; ++a)(c = e.xaxes[a]) && !c.tickColor && (c.tickColor = c.color), c = m.extend(!0, {}, e.xaxis, c), e.xaxes[a] = c, c.font && (c.font = m.extend({}, d, c.font), c.font.color || (c.font.color = c.color), c.font.lineHeight || (c.font.lineHeight = Math.round(1.15 *
                c.font.size)));
            b = e.yaxes.length || 1;
            for (a = 0; a < b; ++a)(c = e.yaxes[a]) && !c.tickColor && (c.tickColor = c.color), c = m.extend(!0, {}, e.yaxis, c), e.yaxes[a] = c, c.font && (c.font = m.extend({}, d, c.font), c.font.color || (c.font.color = c.color), c.font.lineHeight || (c.font.lineHeight = Math.round(1.15 * c.font.size)));
            e.xaxis.noTicks && null == e.xaxis.ticks && (e.xaxis.ticks = e.xaxis.noTicks);
            e.yaxis.noTicks && null == e.yaxis.ticks && (e.yaxis.ticks = e.yaxis.noTicks);
            e.x2axis && (e.xaxes[1] = m.extend(!0, {}, e.xaxis, e.x2axis), e.xaxes[1].position =
                "top", null == e.x2axis.min && (e.xaxes[1].min = null), null == e.x2axis.max && (e.xaxes[1].max = null));
            e.y2axis && (e.yaxes[1] = m.extend(!0, {}, e.yaxis, e.y2axis), e.yaxes[1].position = "right", null == e.y2axis.min && (e.yaxes[1].min = null), null == e.y2axis.max && (e.yaxes[1].max = null));
            e.grid.coloredAreas && (e.grid.markings = e.grid.coloredAreas);
            e.grid.coloredAreasColor && (e.grid.markingsColor = e.grid.coloredAreasColor);
            e.lines && m.extend(!0, e.series.lines, e.lines);
            e.points && m.extend(!0, e.series.points, e.points);
            e.bars && m.extend(!0,
                e.series.bars, e.bars);
            null != e.shadowSize && (e.series.shadowSize = e.shadowSize);
            null != e.highlightColor && (e.series.highlightColor = e.highlightColor);
            for (a = 0; a < e.xaxes.length; ++a) L(E, a + 1).options = e.xaxes[a];
            for (a = 0; a < e.yaxes.length; ++a) L(I, a + 1).options = e.yaxes[a];
            for (var f in G) e.hooks[f] && e.hooks[f].length && (G[f] = G[f].concat(e.hooks[f]));
            s(G.processOptions, [e])
        })(k);
        (function () {
            g.css("padding", 0).children().filter(function () {
                return !m(this).hasClass("flot-overlay") && !m(this).hasClass("flot-base")
            }).remove();
            "static" == g.css("position") && g.css("position", "relative");
            B = new C("flot-base", g);
            Q = new C("flot-overlay", g);
            l = B.context;
            A = Q.context;
            M = m(Q.element).unbind();
            var a = g.data("plot");
            a && (a.shutdown(), Q.clear());
            g.data("plot", x)
        })();
        K(h);
        aa();
        ba();
        e.grid.hoverable && (M.mousemove(Y), M.bind("mouseleave", Z));
        e.grid.clickable && M.click($);
        s(G.bindEvents, [M]);
        var O = [],
            R = null
    }

    var p = Object.prototype.hasOwnProperty;
    m.fn.detach || (m.fn.detach = function () {
        return this.each(function () {
            this.parentNode && this.parentNode.removeChild(this)
        })
    });
    C.prototype.resize = function (g, h) {
        if (0 >= g || 0 >= h) throw Error("Invalid dimensions for plot, width = " + g + ", height = " + h);
        var k = this.element,
            m = this.context,
            p = this.pixelRatio;
        this.width != g && (k.width = g * p, k.style.width = g + "px", this.width = g);
        this.height != h && (k.height = h * p, k.style.height = h + "px", this.height = h);
        m.restore();
        m.save();
        m.scale(p, p)
    };
    C.prototype.clear = function () {
        this.context.clearRect(0, 0, this.width, this.height)
    };
    C.prototype.render = function () {
        var g = this._textCache,
            h;
        for (h in g)
            if (p.call(g, h)) {
                var k =
                        this.getTextLayer(h),
                    m = g[h];
                k.hide();
                for (var s in m)
                    if (p.call(m, s)) {
                        var u = m[s],
                            z;
                        for (z in u)
                            if (p.call(u, z)) {
                                for (var F = u[z].positions, C = 0, L; L = F[C]; C++) L.active ? L.rendered || (k.append(L.element), L.rendered = !0) : (F.splice(C--, 1), L.rendered && L.element.detach());
                                0 == F.length && delete u[z]
                            }
                    }
                k.show()
            }
    };
    C.prototype.getTextLayer = function (g) {
        var h = this.text[g];
        null == h && (null == this.textContainer && (this.textContainer = m("<div class='flot-text'></div>").css({
            position: "absolute",
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            "font-size": "smaller",
            color: "#545454"
        }).insertAfter(this.element)), h = this.text[g] = m("<div></div>").addClass(g).css({
            position: "absolute",
            top: 0,
            left: 0,
            bottom: 0,
            right: 0
        }).appendTo(this.textContainer));
        return h
    };
    C.prototype.getTextInfo = function (g, h, k, p, s) {
        var u, z;
        h = "" + h;
        p = "object" === typeof k ? k.style + " " + k.variant + " " + k.weight + " " + k.size + "px/" + k.lineHeight + "px " + k.family : k;
        u = this._textCache[g];
        null == u && (u = this._textCache[g] = {});
        z = u[p];
        null == z && (z = u[p] = {});
        u = z[h];
        null == u && (g = m("<div></div>").html(h).css({
            position: "absolute",
            "max-width": s,
            top: -9999
        }).appendTo(this.getTextLayer(g)), "object" === typeof k ? g.css({
            font: p,
            color: k.color
        }) : "string" === typeof k && g.addClass(k), u = z[h] = {
            width: g.outerWidth(!0),
            height: g.outerHeight(!0),
            element: g,
            positions: []
        }, g.detach());
        return u
    };
    C.prototype.addText = function (g, h, k, m, p, u, z, F, C) {
        g = this.getTextInfo(g, m, p, u, z);
        m = g.positions;
        "center" == F ? h -= g.width / 2 : "right" == F && (h -= g.width);
        "middle" == C ? k -= g.height / 2 : "bottom" == C && (k -= g.height);
        for (C = 0; p = m[C]; C++)
            if (p.x == h && p.y == k) {
                p.active = !0;
                return
            }
        p = {
            active: !0,
            rendered: !1,
            element: m.length ? g.element.clone() : g.element,
            x: h,
            y: k
        };
        m.push(p);
        p.element.css({
            top: Math.round(k),
            left: Math.round(h),
            "text-align": F
        })
    };
    C.prototype.removeText = function (g, h, k, m, s, u) {
        if (null == m) {
            if (h = this._textCache[g], null != h)
                for (var z in h)
                    if (p.call(h, z)) {
                        k = h[z];
                        for (var C in k)
                            if (p.call(k, C))
                                for (g = k[C].positions, m = 0; s = g[m]; m++) s.active = !1
                    }
        } else
            for (g = this.getTextInfo(g, m, s, u).positions, m = 0; s = g[m]; m++) s.x == h && s.y == k && (s.active = !1)
    };
    m.plot = function (g, h, k) {
        return new u(m(g), h, k, m.plot.plugins)
    };
    m.plot.version = "0.8.3";
    m.plot.plugins = [];
    m.fn.plot = function (g, h) {
        return this.each(function () {
            m.plot(this, g, h)
        })
    }
})(jQuery);