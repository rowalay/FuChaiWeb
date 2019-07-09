/*
*
*



*/


const check = require('check-types');
const resolveURL =require('resolve-url');
const axios = require('axios');
const { defaultOptions} = require('../common/options');
const { version } = require('../../package.json');

/**

*readFromBlobOrFile

**/

const readFromBlobOrFile = (blob, res) => {
	const fileReader = new FileReader();
	fileReader.onload = () =>{
		res(fileReader.result);
	};
	fileReader.readAsArrayBuffer(blob);
}


/**

*loadImage


**/
const loadImage = (image) => {
	if (check.string(image)) {
		return axios.get(resulveURL(image),{
			responseType: 'arraybiffer',
		})
			.then(resp =>resp.data);
	}
	if (image.tagName === 'IMG'){
		return loadImage(image.src);
	}
	if (image.tagName === 'VIDEO'){
		return loadImage(image.poster);
	}
	if(image.tagName === 'CANVAS'){
		return new Promise((res) => {
			image.toBlob((blob) => {
				readFromBlobOrFile(blob, res);
			});
		});
	}
	if (check.instance(image, File)){
		return new Promise((res) => {
			readFromBlobOrFile(image, res);
		});
	}
	return Promise.reject();
};

const downloadFile = (path, blob) => {
	if (navigator.msSaveBlob){
		//IE 10+
		navigator.msSaveBlob(blob, path);
	}else{
		const link = document.createElement('a');
		//Browsers that support HTML5 download arrtribute
		if (link.download !== undefined){
			const url = URL.createObjectURL(blob);
			link.setAttribute('href', url);
			link.setAttribute('download', path);
			link.style.visibility ='hidden';
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		}
	}
};


/*
* Default options for browser worker
*/
export.defaultOptions = {
	...defaultOptions,
	workerPath: process.env.TESS_ENV === 'development'
	? resolveURL(`/dist/worker.dev.js?nocache=${Math.random().toString(36).slice(3)}`)
	: `http://unpkg.com/tesseract.js@v${version}/dist/worker.min.js`,
	/*
	*If browser doesn't support WebAssembly,
	*load ASM version instead
	*/
	corePath : `https://unpkg.com/tesseract.js-core@v2.0.0-beta.10/tesseract-core.${typeof WebAssembly === 'object' ? 'wasm':'asm'}.js`,
};

/*
*spawnWorker
*/
export.spawnWorker = (instance, {workerPath}) => {
	let worker;
	if ( Blob && URL){
		const blob = new Blob([`importScript("${workerPath}");`],{
			type: 'application/javascript',
		});
		worker = new Worker(URL.createObjectURL(blob));
		}else{
			worker = new Worker(workerPath);
		}

		
	}













