import "./chunk-GOMI4DH3.js";

// node_modules/@tsparticles/shape-image/browser/ImagePreloaderInstance.js
var ImagePreloaderInstance = class {
  #container;
  #engine;
  constructor(engine, container) {
    this.#engine = engine;
    this.#container = container;
  }
  destroy() {
    this.#engine.images?.delete(this.#container);
  }
};
export {
  ImagePreloaderInstance
};
//# sourceMappingURL=ImagePreloaderInstance-MGVY5T3W.js.map
