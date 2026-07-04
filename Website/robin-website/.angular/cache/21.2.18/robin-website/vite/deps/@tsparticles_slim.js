import {
  DivType,
  Interactivity,
  InteractorType,
  mouseLeaveEvent,
  mouseMoveEvent
} from "./chunk-TPMEKHZB.js";
import {
  DestroyType,
  RotateDirection
} from "./chunk-Z7RUR3RC.js";
import {
  AnimatableColor,
  AnimationMode,
  AnimationStatus,
  Circle,
  OptionsColor,
  OutMode,
  OutModeDirection,
  ParticleOutType,
  ParticlesBounce,
  RangedAnimationOptions,
  RangedAnimationValueWithRandom,
  Rectangle,
  StartValueType,
  ValueWithRandom,
  Vector,
  calculateBounds,
  circleBounce,
  circleBounceDataFromParticle,
  clamp,
  colorMix,
  deepExtend,
  defaultAlpha,
  defaultRatio,
  degToRad,
  double,
  doublePI,
  executeOnSingleOrMultiple,
  getDistance,
  getDistances,
  getHslAnimationFromHsl,
  getItemMapFromInitializer,
  getItemsFromInitializer,
  getLinkColor,
  getLinkRandomColor,
  getLogger,
  getRandom,
  getRangeMax,
  getRangeMin,
  getRangeValue,
  getStyleFromHsl,
  getStyleFromRgb,
  half,
  hslToRgb,
  hslaToRgba,
  identity,
  isArray,
  isInArray,
  isNull,
  isObject,
  isPointInside,
  itemFromArray,
  itemFromSingleOrMultiple,
  loadOptionProperty,
  loadProperty,
  loadRangeProperty,
  millisecondsToSeconds,
  minDistance,
  minRadius,
  minVelocity,
  originPoint,
  parseAlpha,
  percentDenominator,
  randomInRangeValue,
  rangeColorToHsl,
  rgbToHsl,
  safeDocument,
  setRangeValue,
  squareExp,
  updateColor
} from "./chunk-DGIMIMD3.js";
import {
  __spreadProps,
  __spreadValues
} from "./chunk-GOMI4DH3.js";

// node_modules/@tsparticles/plugin-blend/browser/Options/Classes/Blend.js
var Blend = class {
  enable = false;
  mode = "destination-out";
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "mode", data.mode);
    loadProperty(this, "enable", data.enable);
  }
};

// node_modules/@tsparticles/plugin-blend/browser/BlendPlugin.js
var BlendPlugin = class {
  id = "blend";
  async getPlugin(container) {
    const { BlendPluginInstance } = await import("./BlendPluginInstance-5M7YYL7C.js");
    return new BlendPluginInstance(container);
  }
  loadOptions(_container, options, source) {
    if (!this.needsPlugin(options) && !this.needsPlugin(source)) {
      return;
    }
    let blendOptions = options.blend;
    if (!blendOptions?.load) {
      options.blend = blendOptions = new Blend();
    }
    blendOptions.load(source?.blend);
  }
  loadParticlesOptions(_container, options, source) {
    options.blend ??= new Blend();
    options.blend.load(source?.blend);
  }
  needsPlugin(options) {
    return !!options?.blend?.enable || !!options?.particles?.blend?.enable;
  }
};

// node_modules/@tsparticles/plugin-blend/browser/index.js
async function loadBlendPlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addPlugin(new BlendPlugin());
  });
}

// node_modules/@tsparticles/shape-circle/browser/Utils.js
var minAngle = 0;
function drawCircle(data) {
  const { context, particle, radius } = data;
  particle.circleRange ??= { min: minAngle, max: doublePI };
  const circleRange = particle.circleRange;
  context.arc(originPoint.x, originPoint.y, radius, circleRange.min, circleRange.max, false);
}

// node_modules/@tsparticles/shape-circle/browser/CircleDrawer.js
var sides = 12;
var maxAngle = 360;
var minAngle2 = 0;
var CircleDrawer = class {
  draw(data) {
    drawCircle(data);
  }
  getSidesCount() {
    return sides;
  }
  particleInit(_container, particle) {
    const shapeData = particle.shapeData, angle = shapeData?.angle ?? {
      max: maxAngle,
      min: minAngle2
    };
    particle.circleRange = isObject(angle) ? { min: degToRad(angle.min), max: degToRad(angle.max) } : {
      min: minAngle2,
      max: degToRad(angle)
    };
  }
};

// node_modules/@tsparticles/shape-circle/browser/index.js
async function loadCircleShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(["circle"], () => {
      return Promise.resolve(new CircleDrawer());
    });
  });
}

// node_modules/@tsparticles/plugin-hex-color/browser/HexColorManager.js
var RgbIndexes;
(function(RgbIndexes3) {
  RgbIndexes3[RgbIndexes3["r"] = 1] = "r";
  RgbIndexes3[RgbIndexes3["g"] = 2] = "g";
  RgbIndexes3[RgbIndexes3["b"] = 3] = "b";
  RgbIndexes3[RgbIndexes3["a"] = 4] = "a";
})(RgbIndexes || (RgbIndexes = {}));
var shorthandHexRegex = /^#?([a-f\d])([a-f\d])([a-f\d])([a-f\d])?$/i;
var hexRegex = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})?$/i;
var hexRadix = 16;
var defaultAlpha2 = 1;
var alphaFactor = 255;
var HexColorManager = class {
  accepts(input) {
    return input.startsWith("#");
  }
  handleColor(color) {
    return this.#parseString(color.value);
  }
  handleRangeColor(color) {
    return this.#parseString(color.value);
  }
  parseString(input) {
    return this.#parseString(input);
  }
  #parseString(hexColor) {
    if (typeof hexColor !== "string" || !this.accepts(hexColor)) {
      return;
    }
    const hexFixed = hexColor.replace(shorthandHexRegex, (_, r, g, b, a) => {
      return r + r + g + g + b + b + (a === void 0 ? "" : a + a);
    }), result = hexRegex.exec(hexFixed);
    return result ? {
      a: result[RgbIndexes.a] ? Number.parseInt(result[RgbIndexes.a], hexRadix) / alphaFactor : defaultAlpha2,
      b: Number.parseInt(result[RgbIndexes.b] ?? "0", hexRadix),
      g: Number.parseInt(result[RgbIndexes.g] ?? "0", hexRadix),
      r: Number.parseInt(result[RgbIndexes.r] ?? "0", hexRadix)
    } : void 0;
  }
};

// node_modules/@tsparticles/plugin-hex-color/browser/index.js
async function loadHexColorPlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addColorManager("hex", new HexColorManager());
  });
}

// node_modules/@tsparticles/plugin-hsl-color/browser/HslColorManager.js
var HslIndexes;
(function(HslIndexes2) {
  HslIndexes2[HslIndexes2["h"] = 1] = "h";
  HslIndexes2[HslIndexes2["s"] = 2] = "s";
  HslIndexes2[HslIndexes2["l"] = 3] = "l";
  HslIndexes2[HslIndexes2["a"] = 5] = "a";
})(HslIndexes || (HslIndexes = {}));
var hslRegex = /hsla?\(\s*(\d+)\s*[\s,]\s*(\d+)%\s*[\s,]\s*(\d+)%\s*([\s,]\s*(0|1|0?\.\d+|(\d{1,3})%)\s*)?\)/i;
var HslColorManager = class {
  accepts(input) {
    return input.startsWith("hsl");
  }
  handleColor(color) {
    const colorValue = color.value, hslColor = colorValue.hsl ?? color.value;
    if (!("h" in hslColor) || !("s" in hslColor) || !("l" in hslColor)) {
      return;
    }
    return hslToRgb(hslColor);
  }
  handleRangeColor(color) {
    const colorValue = color.value, hslColor = colorValue.hsl ?? color.value;
    if (!("h" in hslColor) || !("s" in hslColor) || !("l" in hslColor)) {
      return;
    }
    return hslToRgb({
      h: getRangeValue(hslColor.h),
      l: getRangeValue(hslColor.l),
      s: getRangeValue(hslColor.s)
    });
  }
  parseString(input) {
    if (!this.accepts(input)) {
      return;
    }
    const result = hslRegex.exec(input), minLength = 4, defaultAlpha3 = 1, radix = 10;
    return result ? hslaToRgba({
      a: result.length > minLength ? parseAlpha(result[HslIndexes.a]) : defaultAlpha3,
      h: Number.parseInt(result[HslIndexes.h] ?? "0", radix),
      l: Number.parseInt(result[HslIndexes.l] ?? "0", radix),
      s: Number.parseInt(result[HslIndexes.s] ?? "0", radix)
    }) : void 0;
  }
};

// node_modules/@tsparticles/plugin-hsl-color/browser/index.js
async function loadHslColorPlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addColorManager("hsl", new HslColorManager());
  });
}

// node_modules/@tsparticles/plugin-move/browser/MovePlugin.js
var MovePlugin = class {
  id = "move";
  #pluginManager;
  constructor(pluginManager) {
    this.#pluginManager = pluginManager;
  }
  async getPlugin(container) {
    const { MovePluginInstance } = await import("./MovePluginInstance-BYBHF4LL.js");
    return new MovePluginInstance(this.#pluginManager, container);
  }
  loadOptions() {
  }
  needsPlugin() {
    return true;
  }
};

// node_modules/@tsparticles/plugin-move/browser/index.js
async function loadMovePlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    const moveEngine = e, movePluginManager = moveEngine.pluginManager;
    movePluginManager.initializers.pathGenerators ??= /* @__PURE__ */ new Map();
    movePluginManager.pathGenerators ??= /* @__PURE__ */ new Map();
    movePluginManager.addPathGenerator = (name, generator) => {
      movePluginManager.initializers.pathGenerators ??= /* @__PURE__ */ new Map();
      movePluginManager.initializers.pathGenerators.set(name, generator);
    };
    movePluginManager.getPathGenerators = async (container, force = false) => {
      movePluginManager.initializers.pathGenerators ??= /* @__PURE__ */ new Map();
      movePluginManager.pathGenerators ??= /* @__PURE__ */ new Map();
      return getItemMapFromInitializer(container, movePluginManager.pathGenerators, movePluginManager.initializers.pathGenerators, force);
    };
    e.pluginManager.addPlugin(new MovePlugin(e.pluginManager));
  });
}

// node_modules/@tsparticles/animation-utils/browser/Utils.js
function checkDestroy(particle, destroyType, value, minValue, maxValue) {
  switch (destroyType) {
    case DestroyType.max:
      if (value >= maxValue) {
        particle.destroy();
      }
      break;
    case DestroyType.min:
      if (value <= minValue) {
        particle.destroy();
      }
      break;
    default:
      break;
  }
}
function initParticleNumericAnimationValue(options, pxRatio) {
  const valueRange = options.value, animationOptions = options.animation, res = {
    delayTime: getRangeValue(animationOptions.delay) * millisecondsToSeconds,
    enable: animationOptions.enable,
    value: getRangeValue(options.value) * pxRatio,
    max: getRangeMax(valueRange) * pxRatio,
    min: getRangeMin(valueRange) * pxRatio,
    loops: 0,
    maxLoops: getRangeValue(animationOptions.count),
    time: 0
  }, decayOffset = 1;
  if (animationOptions.enable) {
    res.decay = decayOffset - getRangeValue(animationOptions.decay);
    switch (animationOptions.mode) {
      case AnimationMode.increase:
        res.status = AnimationStatus.increasing;
        break;
      case AnimationMode.decrease:
        res.status = AnimationStatus.decreasing;
        break;
      case AnimationMode.random:
        res.status = getRandom() >= half ? AnimationStatus.increasing : AnimationStatus.decreasing;
        break;
      default:
        break;
    }
    const autoStatus = animationOptions.mode === AnimationMode.auto;
    switch (animationOptions.startValue) {
      case StartValueType.min:
        res.value = res.min;
        if (autoStatus) {
          res.status = AnimationStatus.increasing;
        }
        break;
      case StartValueType.max:
        res.value = res.max;
        if (autoStatus) {
          res.status = AnimationStatus.decreasing;
        }
        break;
      case StartValueType.random:
      default:
        res.value = randomInRangeValue(res);
        if (autoStatus) {
          res.status = getRandom() >= half ? AnimationStatus.increasing : AnimationStatus.decreasing;
        }
        break;
    }
  }
  res.initialValue = res.value;
  return res;
}
function updateAnimation(particle, data, changeDirection, destroyType, delta) {
  const minLoops2 = 0, minDelay = 0, identity4 = 1, minVelocity2 = 0, minDecay = 1;
  if (particle.destroyed || !data.enable || (data.maxLoops ?? minLoops2) > minLoops2 && (data.loops ?? minLoops2) > (data.maxLoops ?? minLoops2)) {
    return;
  }
  const velocity = (data.velocity ?? minVelocity2) * delta.factor, minValue = data.min, maxValue = data.max, decay = data.decay ?? minDecay;
  data.time ??= 0;
  const delayTime = data.delayTime ?? minDelay;
  if (delayTime > minDelay && data.time < delayTime) {
    data.time += delta.value;
    if (data.time < delayTime) {
      return;
    }
  }
  switch (data.status) {
    case AnimationStatus.increasing:
      data.value += velocity;
      break;
    case AnimationStatus.decreasing:
      data.value -= velocity;
      break;
    default:
      break;
  }
  if (data.velocity && decay !== identity4) {
    data.velocity *= decay;
  }
  switch (data.status) {
    case AnimationStatus.increasing:
      if (data.value >= maxValue) {
        if (changeDirection) {
          data.status = AnimationStatus.decreasing;
        } else {
          data.value -= maxValue;
        }
        data.loops ??= minLoops2;
        data.loops++;
      }
      break;
    case AnimationStatus.decreasing:
      if (data.value <= minValue) {
        if (changeDirection) {
          data.status = AnimationStatus.increasing;
        } else {
          data.value += maxValue;
        }
        data.loops ??= minLoops2;
        data.loops++;
      }
      break;
    default:
      break;
  }
  checkDestroy(particle, destroyType, data.value, minValue, maxValue);
  if (!particle.destroyed) {
    data.value = clamp(data.value, minValue, maxValue);
  }
}

// node_modules/@tsparticles/updater-opacity/browser/Options/Classes/OpacityAnimation.js
var OpacityAnimation = class extends RangedAnimationOptions {
  destroy = DestroyType.none;
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "destroy", data.destroy);
  }
};

// node_modules/@tsparticles/updater-opacity/browser/Options/Classes/Opacity.js
var Opacity = class extends RangedAnimationValueWithRandom {
  animation = new OpacityAnimation();
  value = 1;
  load(data) {
    if (isNull(data)) {
      return;
    }
    super.load(data);
    const animation = data.animation;
    if (animation !== void 0) {
      this.animation.load(animation);
    }
  }
};

// node_modules/@tsparticles/updater-opacity/browser/OpacityUpdater.js
var OpacityUpdater = class {
  #container;
  constructor(container) {
    this.#container = container;
  }
  init(particle) {
    const opacityOptions = particle.options.opacity, pxRatio = 1;
    if (!opacityOptions) {
      return;
    }
    particle.opacity = initParticleNumericAnimationValue(opacityOptions, pxRatio);
    const opacityAnimation = opacityOptions.animation;
    if (opacityAnimation.enable) {
      particle.opacity.velocity = getRangeValue(opacityAnimation.speed) / percentDenominator * this.#container.retina.reduceFactor;
      if (!opacityAnimation.sync) {
        particle.opacity.velocity *= getRandom();
      }
    }
  }
  isEnabled(particle) {
    const none = 0;
    return !particle.destroyed && !particle.spawning && !!particle.opacity && particle.opacity.enable && ((particle.opacity.maxLoops ?? none) <= none || (particle.opacity.maxLoops ?? none) > none && (particle.opacity.loops ?? none) < (particle.opacity.maxLoops ?? none));
  }
  loadOptions(options, ...sources) {
    loadOptionProperty(options, "opacity", Opacity, ...sources);
  }
  reset(particle) {
    if (!particle.opacity) {
      return;
    }
    particle.opacity.time = 0;
    particle.opacity.loops = 0;
  }
  update(particle, delta) {
    if (!this.isEnabled(particle) || !particle.opacity || !particle.options.opacity) {
      return;
    }
    updateAnimation(particle, particle.opacity, true, particle.options.opacity.animation.destroy, delta);
  }
};

// node_modules/@tsparticles/updater-opacity/browser/index.js
async function loadOpacityUpdater(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addParticleUpdater("opacity", (container) => {
      return Promise.resolve(new OpacityUpdater(container));
    });
  });
}

// node_modules/@tsparticles/updater-out-modes/browser/Utils.js
var boundsMin = 0;
function bounceHorizontal(data) {
  if (data.outMode !== OutMode.bounce && data.outMode !== OutMode.split || data.direction !== OutModeDirection.left && data.direction !== OutModeDirection.right) {
    return;
  }
  if (data.bounds.right < boundsMin && data.direction === OutModeDirection.left) {
    data.particle.position.x = data.size + data.offset.x;
  } else if (data.bounds.left > data.canvasSize.width && data.direction === OutModeDirection.right) {
    data.particle.position.x = data.canvasSize.width - data.size - data.offset.x;
  }
  const velocity = data.particle.velocity.x;
  let bounced = false;
  if (data.outOfCanvas && (data.direction === OutModeDirection.right && velocity > minVelocity || data.direction === OutModeDirection.left && velocity < minVelocity)) {
    const newVelocity = getRangeValue(data.particle.options.bounce.horizontal.value);
    data.particle.velocity.x *= -newVelocity;
    bounced = true;
  }
  if (!bounced) {
    return;
  }
  const minPos = data.offset.x + data.size;
  if (data.outOfCanvas && data.direction === OutModeDirection.right) {
    data.particle.position.x = data.canvasSize.width - minPos;
  } else if (data.outOfCanvas && data.direction === OutModeDirection.left) {
    data.particle.position.x = minPos;
  }
  if (data.outMode === OutMode.split) {
    data.particle.destroy();
  }
}
function bounceVertical(data) {
  if (data.outMode !== OutMode.bounce && data.outMode !== OutMode.split || data.direction !== OutModeDirection.bottom && data.direction !== OutModeDirection.top) {
    return;
  }
  if (data.bounds.bottom < boundsMin && data.direction === OutModeDirection.top) {
    data.particle.position.y = data.size + data.offset.y;
  } else if (data.bounds.top > data.canvasSize.height && data.direction === OutModeDirection.bottom) {
    data.particle.position.y = data.canvasSize.height - data.size - data.offset.y;
  }
  const velocity = data.particle.velocity.y;
  let bounced = false;
  if (data.outOfCanvas && (data.direction === OutModeDirection.bottom && velocity > minVelocity || data.direction === OutModeDirection.top && velocity < minVelocity)) {
    const newVelocity = getRangeValue(data.particle.options.bounce.vertical.value);
    data.particle.velocity.y *= -newVelocity;
    bounced = true;
  }
  if (!bounced) {
    return;
  }
  const minPos = data.offset.y + data.size;
  if (data.outOfCanvas && data.direction === OutModeDirection.bottom) {
    data.particle.position.y = data.canvasSize.height - minPos;
  } else if (data.outOfCanvas && data.direction === OutModeDirection.top) {
    data.particle.position.y = minPos;
  }
  if (data.outMode === OutMode.split) {
    data.particle.destroy();
  }
}

// node_modules/@tsparticles/updater-out-modes/browser/BounceOutMode.js
var BounceOutMode = class {
  modes;
  #container;
  #particleBouncePlugins;
  constructor(container) {
    this.#container = container;
    this.modes = [
      OutMode.bounce,
      OutMode.split
    ];
    this.#particleBouncePlugins = container.plugins.filter((p) => p.particleBounce !== void 0);
  }
  update(particle, direction, delta, outMode) {
    if (!this.modes.includes(outMode)) {
      return;
    }
    const container = this.#container;
    let handled = false;
    for (const plugin of this.#particleBouncePlugins) {
      handled = plugin.particleBounce?.(particle, delta, direction) ?? false;
      if (handled) {
        break;
      }
    }
    if (handled) {
      return;
    }
    const pos = particle.getPosition(), offset = particle.offset, size = particle.getRadius(), bounds = calculateBounds(pos, size), canvasSize = container.canvas.size, outOfCanvas = !particle.isInsideCanvasForOutMode(outMode, direction);
    bounceHorizontal({ particle, outMode, direction, bounds, canvasSize, offset, outOfCanvas, size });
    bounceVertical({ particle, outMode, direction, bounds, canvasSize, offset, outOfCanvas, size });
  }
};

// node_modules/@tsparticles/updater-out-modes/browser/DestroyOutMode.js
var DestroyOutMode = class {
  modes;
  constructor(_container) {
    this.modes = [OutMode.destroy];
  }
  update(particle, direction, _delta, outMode) {
    if (!this.modes.includes(outMode)) {
      return;
    }
    switch (particle.outType) {
      case ParticleOutType.normal:
      case ParticleOutType.outside:
        if (particle.isInsideCanvasForOutMode(outMode, direction)) {
          return;
        }
        break;
      case ParticleOutType.inside: {
        const { dx, dy } = getDistances(particle.position, particle.moveCenter), { x: vx, y: vy } = particle.velocity;
        if (vx < minVelocity && dx > particle.moveCenter.radius || vy < minVelocity && dy > particle.moveCenter.radius || vx >= minVelocity && dx < -particle.moveCenter.radius || vy >= minVelocity && dy < -particle.moveCenter.radius) {
          return;
        }
        break;
      }
    }
    particle.destroy(true);
  }
};

// node_modules/@tsparticles/updater-out-modes/browser/NoneOutMode.js
var NoneOutMode = class {
  modes;
  #container;
  constructor(container) {
    this.#container = container;
    this.modes = [OutMode.none];
  }
  update(particle, direction, _delta, outMode) {
    if (!this.modes.includes(outMode)) {
      return;
    }
    if ((particle.options.move.distance.horizontal && (direction === OutModeDirection.left || direction === OutModeDirection.right)) ?? (particle.options.move.distance.vertical && (direction === OutModeDirection.top || direction === OutModeDirection.bottom))) {
      return;
    }
    const gravityOptions = particle.options.move.gravity, container = this.#container, canvasSize = container.canvas.size, pRadius = particle.getRadius();
    if (!gravityOptions.enable) {
      if (particle.velocity.y > minVelocity && particle.position.y <= canvasSize.height + pRadius || particle.velocity.y < minVelocity && particle.position.y >= -pRadius || particle.velocity.x > minVelocity && particle.position.x <= canvasSize.width + pRadius || particle.velocity.x < minVelocity && particle.position.x >= -pRadius) {
        return;
      }
      if (!isPointInside(particle.position, container.canvas.size, originPoint, pRadius, direction)) {
        particle.destroy();
      }
    } else {
      const position = particle.position;
      if (!gravityOptions.inverse && position.y > canvasSize.height + pRadius && direction === OutModeDirection.bottom || gravityOptions.inverse && position.y < -pRadius && direction === OutModeDirection.top) {
        particle.destroy();
      }
    }
  }
};

// node_modules/@tsparticles/updater-out-modes/browser/OutOutMode.js
var updateVector = Vector.origin;
var OutOutMode = class {
  modes;
  #container;
  constructor(container) {
    this.#container = container;
    this.modes = [OutMode.out];
  }
  update(particle, direction, _delta, outMode) {
    if (!this.modes.includes(outMode)) {
      return;
    }
    const container = this.#container;
    switch (particle.outType) {
      case ParticleOutType.inside: {
        const { x: vx, y: vy } = particle.velocity;
        updateVector.setTo(originPoint);
        updateVector.length = particle.moveCenter.radius;
        updateVector.angle = particle.velocity.angle + Math.PI;
        updateVector.addTo(particle.moveCenter);
        const { dx, dy } = getDistances(particle.position, updateVector);
        if (vx <= minVelocity && dx >= minDistance || vy <= minVelocity && dy >= minDistance || vx >= minVelocity && dx <= minDistance || vy >= minVelocity && dy <= minDistance) {
          return;
        }
        particle.position.x = Math.floor(randomInRangeValue({
          min: 0,
          max: container.canvas.size.width
        }));
        particle.position.y = Math.floor(randomInRangeValue({
          min: 0,
          max: container.canvas.size.height
        }));
        const { dx: newDx, dy: newDy } = getDistances(particle.position, particle.moveCenter);
        particle.direction = Math.atan2(-newDy, -newDx);
        particle.velocity.angle = particle.direction;
        particle.justWarped = true;
        break;
      }
      default: {
        if (particle.isInsideCanvasForOutMode(outMode, direction)) {
          return;
        }
        switch (particle.outType) {
          case ParticleOutType.outside: {
            particle.position.x = Math.floor(randomInRangeValue({
              min: -particle.moveCenter.radius,
              max: particle.moveCenter.radius
            })) + particle.moveCenter.x;
            particle.position.y = Math.floor(randomInRangeValue({
              min: -particle.moveCenter.radius,
              max: particle.moveCenter.radius
            })) + particle.moveCenter.y;
            const { dx, dy } = getDistances(particle.position, particle.moveCenter);
            if (particle.moveCenter.radius) {
              particle.direction = Math.atan2(dy, dx);
              particle.velocity.angle = particle.direction;
            }
            particle.justWarped = true;
            break;
          }
          case ParticleOutType.normal: {
            const warp = particle.options.move.warp, canvasSize = container.canvas.size, newPos = {
              bottom: canvasSize.height + particle.getRadius() + particle.offset.y,
              left: -particle.getRadius() - particle.offset.x,
              right: canvasSize.width + particle.getRadius() + particle.offset.x,
              top: -particle.getRadius() - particle.offset.y
            }, sizeValue = particle.getRadius(), nextBounds = calculateBounds(particle.position, sizeValue);
            if (direction === OutModeDirection.right && nextBounds.left > canvasSize.width + particle.offset.x) {
              particle.position.x = newPos.left;
              particle.initialPosition.x = particle.position.x;
              if (!warp) {
                particle.position.y = getRandom() * canvasSize.height;
                particle.initialPosition.y = particle.position.y;
              }
              particle.justWarped = true;
            } else if (direction === OutModeDirection.left && nextBounds.right < -particle.offset.x) {
              particle.position.x = newPos.right;
              particle.initialPosition.x = particle.position.x;
              if (!warp) {
                particle.position.y = getRandom() * canvasSize.height;
                particle.initialPosition.y = particle.position.y;
              }
              particle.justWarped = true;
            }
            if (direction === OutModeDirection.bottom && nextBounds.top > canvasSize.height + particle.offset.y) {
              if (!warp) {
                particle.position.x = getRandom() * canvasSize.width;
                particle.initialPosition.x = particle.position.x;
              }
              particle.position.y = newPos.top;
              particle.initialPosition.y = particle.position.y;
              particle.justWarped = true;
            } else if (direction === OutModeDirection.top && nextBounds.bottom < -particle.offset.y) {
              if (!warp) {
                particle.position.x = getRandom() * canvasSize.width;
                particle.initialPosition.x = particle.position.x;
              }
              particle.position.y = newPos.bottom;
              particle.initialPosition.y = particle.position.y;
              particle.justWarped = true;
            }
            break;
          }
        }
        break;
      }
    }
  }
};

// node_modules/@tsparticles/updater-out-modes/browser/OutOfCanvasUpdater.js
var checkOutMode = (outModes, outMode) => {
  return outModes.default === outMode || outModes.bottom === outMode || outModes.left === outMode || outModes.right === outMode || outModes.top === outMode;
};
var OutOfCanvasUpdater = class {
  updaters;
  #container;
  constructor(container) {
    this.#container = container;
    this.updaters = /* @__PURE__ */ new Map();
  }
  init(particle) {
    this.#addUpdaterIfMissing(particle, OutMode.bounce, (container) => new BounceOutMode(container));
    this.#addUpdaterIfMissing(particle, OutMode.out, (container) => new OutOutMode(container));
    this.#addUpdaterIfMissing(particle, OutMode.destroy, (container) => new DestroyOutMode(container));
    this.#addUpdaterIfMissing(particle, OutMode.none, (container) => new NoneOutMode(container));
  }
  isEnabled(particle) {
    return !particle.destroyed && !particle.spawning;
  }
  update(particle, delta) {
    const outModes = particle.options.move.outModes;
    particle.justWarped = false;
    this.#updateOutMode(particle, delta, outModes.bottom ?? outModes.default, OutModeDirection.bottom);
    this.#updateOutMode(particle, delta, outModes.left ?? outModes.default, OutModeDirection.left);
    this.#updateOutMode(particle, delta, outModes.right ?? outModes.default, OutModeDirection.right);
    this.#updateOutMode(particle, delta, outModes.top ?? outModes.default, OutModeDirection.top);
  }
  #addUpdaterIfMissing(particle, outMode, getUpdater) {
    const outModes = particle.options.move.outModes;
    if (!this.updaters.has(outMode) && checkOutMode(outModes, outMode)) {
      this.updaters.set(outMode, getUpdater(this.#container));
    }
  }
  #updateOutMode(particle, delta, outMode, direction) {
    for (const updater of this.updaters.values()) {
      updater.update(particle, direction, delta, outMode);
    }
  }
};

// node_modules/@tsparticles/updater-out-modes/browser/index.js
async function loadOutModesUpdater(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addParticleUpdater("outModes", (container) => {
      return Promise.resolve(new OutOfCanvasUpdater(container));
    });
  });
}

// node_modules/@tsparticles/updater-paint/browser/PaintUpdater.js
var defaultOpacity = 1;
var PaintUpdater = class {
  #container;
  #pluginManager;
  constructor(pluginManager, container) {
    this.#container = container;
    this.#pluginManager = pluginManager;
  }
  init(particle) {
    const container = this.#container, options = particle.options, paint = itemFromSingleOrMultiple(options.paint, particle.id, options.reduceDuplicates), color = paint?.color, paintColor = color ?? void 0, fill = paint?.fill, stroke = paint?.stroke;
    if (fill) {
      const fillColor = AnimatableColor.create(paintColor === void 0 ? void 0 : AnimatableColor.create(void 0, paintColor), fill.color);
      particle.fillEnabled = fill.enable;
      particle.fillOpacity = getRangeValue(fill.opacity);
      particle.fillAnimation = fillColor.animation;
      const fillHslColor = rangeColorToHsl(this.#pluginManager, fillColor);
      if (fillHslColor) {
        particle.fillColor = getHslAnimationFromHsl(fillHslColor, particle.fillAnimation, container.retina.reduceFactor);
      }
    } else {
      particle.fillEnabled = false;
      particle.fillAnimation = void 0;
      particle.fillColor = void 0;
      particle.fillOpacity = defaultOpacity;
    }
    if (stroke) {
      const strokeColor = AnimatableColor.create(paintColor === void 0 ? void 0 : AnimatableColor.create(void 0, paintColor), stroke.color);
      particle.strokeWidth = getRangeValue(stroke.width) * container.retina.pixelRatio;
      particle.strokeOpacity = getRangeValue(stroke.opacity ?? defaultOpacity);
      particle.strokeAnimation = strokeColor.animation;
      const strokeHslColor = rangeColorToHsl(this.#pluginManager, strokeColor) ?? particle.getFillColor();
      if (strokeHslColor) {
        particle.strokeColor = getHslAnimationFromHsl(strokeHslColor, particle.strokeAnimation, container.retina.reduceFactor);
      }
    } else {
      particle.strokeAnimation = void 0;
      particle.strokeColor = void 0;
      particle.strokeOpacity = defaultOpacity;
      particle.strokeWidth = 0;
    }
  }
  isEnabled(particle) {
    const { fillAnimation, fillColor, strokeAnimation, strokeColor } = particle, fillEnabled = !!fillAnimation && (fillColor?.h.value !== void 0 && fillColor.h.enable || fillColor?.s.value !== void 0 && fillColor.s.enable || fillColor?.l.value !== void 0 && fillColor.l.enable), strokeEnabled = !!strokeAnimation && (strokeColor?.h.value !== void 0 && strokeColor.h.enable || strokeColor?.s.value !== void 0 && strokeColor.s.enable || strokeColor?.l.value !== void 0 && strokeColor.l.enable);
    return !particle.destroyed && !particle.spawning && (fillEnabled || strokeEnabled);
  }
  update(particle, delta) {
    if (!this.isEnabled(particle)) {
      return;
    }
    updateColor(particle.fillColor, delta, this.#container.hdr);
    updateColor(particle.strokeColor, delta, this.#container.hdr);
  }
};

// node_modules/@tsparticles/updater-paint/browser/index.js
async function loadPaintUpdater(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addParticleUpdater("paint", (container) => {
      return Promise.resolve(new PaintUpdater(e.pluginManager, container));
    });
  });
}

// node_modules/@tsparticles/plugin-rgb-color/browser/RgbColorManager.js
var RgbIndexes2;
(function(RgbIndexes3) {
  RgbIndexes3[RgbIndexes3["r"] = 1] = "r";
  RgbIndexes3[RgbIndexes3["g"] = 2] = "g";
  RgbIndexes3[RgbIndexes3["b"] = 3] = "b";
  RgbIndexes3[RgbIndexes3["a"] = 5] = "a";
})(RgbIndexes2 || (RgbIndexes2 = {}));
var rgbRegex = /rgba?\(\s*(\d{1,3})\s*[\s,]\s*(\d{1,3})\s*[\s,]\s*(\d{1,3})\s*([\s,]\s*(0|1|0?\.\d+|(\d{1,3})%)\s*)?\)/i;
var RgbColorManager = class {
  accepts(input) {
    return input.startsWith("rgb");
  }
  handleColor(color) {
    const colorValue = color.value, rgbColor = colorValue.rgb ?? color.value;
    if (!("r" in rgbColor) || !("g" in rgbColor) || !("b" in rgbColor)) {
      return;
    }
    return rgbColor;
  }
  handleRangeColor(color) {
    const colorValue = color.value, rgbColor = colorValue.rgb ?? color.value;
    if (!("r" in rgbColor) || !("g" in rgbColor) || !("b" in rgbColor)) {
      return;
    }
    return {
      r: getRangeValue(rgbColor.r),
      g: getRangeValue(rgbColor.g),
      b: getRangeValue(rgbColor.b)
    };
  }
  parseString(input) {
    if (!this.accepts(input)) {
      return;
    }
    const result = rgbRegex.exec(input), radix = 10, minLength = 4, defaultAlpha3 = 1;
    return result ? {
      a: result.length > minLength ? parseAlpha(result[RgbIndexes2.a]) : defaultAlpha3,
      b: parseInt(result[RgbIndexes2.b] ?? "0", radix),
      g: parseInt(result[RgbIndexes2.g] ?? "0", radix),
      r: parseInt(result[RgbIndexes2.r] ?? "0", radix)
    } : void 0;
  }
};

// node_modules/@tsparticles/plugin-rgb-color/browser/index.js
async function loadRgbColorPlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addColorManager("rgb", new RgbColorManager());
  });
}

// node_modules/@tsparticles/updater-size/browser/Options/Classes/SizeAnimation.js
var SizeAnimation = class extends RangedAnimationOptions {
  destroy = DestroyType.none;
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "destroy", data.destroy);
  }
};

// node_modules/@tsparticles/updater-size/browser/Options/Classes/Size.js
var Size = class extends RangedAnimationValueWithRandom {
  animation = new SizeAnimation();
  value = 3;
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    const animation = data.animation;
    if (animation !== void 0) {
      this.animation.load(animation);
    }
  }
};

// node_modules/@tsparticles/updater-size/browser/SizeUpdater.js
var minLoops = 0;
var SizeUpdater = class {
  #container;
  constructor(container) {
    this.#container = container;
  }
  init(particle) {
    const container = this.#container, sizeOptions = particle.options.size;
    if (!sizeOptions) {
      return;
    }
    const sizeAnimation = sizeOptions.animation;
    if (!sizeAnimation.enable) {
      return;
    }
    particle.size.velocity = particle.retina.sizeAnimationSpeed / percentDenominator * container.retina.reduceFactor;
    if (sizeAnimation.sync) {
      return;
    }
    particle.size.velocity *= getRandom();
  }
  isEnabled(particle) {
    return !particle.destroyed && !particle.spawning && particle.size.enable && ((particle.size.maxLoops ?? minLoops) <= minLoops || (particle.size.maxLoops ?? minLoops) > minLoops && (particle.size.loops ?? minLoops) < (particle.size.maxLoops ?? minLoops));
  }
  loadOptions(options, ...sources) {
    loadOptionProperty(options, "size", Size, ...sources);
  }
  preInit(particle) {
    const pxRatio = this.#container.retina.pixelRatio, options = particle.options, sizeOptions = options.size;
    if (!sizeOptions) {
      return;
    }
    particle.size = initParticleNumericAnimationValue(sizeOptions, pxRatio);
    particle.retina.sizeAnimationSpeed = getRangeValue(sizeOptions.animation.speed) * pxRatio;
  }
  reset(particle) {
    particle.size.time = 0;
    particle.size.loops = 0;
  }
  update(particle, delta) {
    if (!this.isEnabled(particle) || !particle.options.size) {
      return;
    }
    updateAnimation(particle, particle.size, true, particle.options.size.animation.destroy, delta);
  }
};

// node_modules/@tsparticles/updater-size/browser/index.js
async function loadSizeUpdater(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addParticleUpdater("size", (container) => {
      return Promise.resolve(new SizeUpdater(container));
    });
  });
}

// node_modules/@tsparticles/basic/browser/index.js
async function loadBasic(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register(async (e) => {
    await Promise.all([
      loadBlendPlugin(e),
      loadHexColorPlugin(e),
      loadHslColorPlugin(e),
      loadRgbColorPlugin(e),
      loadMovePlugin(e),
      loadCircleShape(e),
      loadPaintUpdater(e),
      loadOpacityUpdater(e),
      loadOutModesUpdater(e),
      loadSizeUpdater(e)
    ]);
  });
}

// node_modules/@tsparticles/plugin-easing-quad/browser/easingsFunctions.js
var easingsFunctions = /* @__PURE__ */ new Map();
easingsFunctions.set("ease-in-quad", (value) => value ** 2);
easingsFunctions.set("ease-out-quad", (value) => 1 - (1 - value) ** 2);
easingsFunctions.set("ease-in-out-quad", (value) => value < 0.5 ? 2 * value ** 2 : 1 - (-2 * value + 2) ** 2 / 2);

// node_modules/@tsparticles/plugin-easing-quad/browser/index.js
async function loadEasingQuadPlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    for (const [easing, easingFn] of easingsFunctions) {
      e.pluginManager.addEasing(easing, easingFn);
    }
  });
}

// node_modules/@tsparticles/shape-emoji/browser/Utils.js
var validTypes = ["emoji"];
function drawEmoji(data, image) {
  const { context, opacity } = data, previousAlpha = context.globalAlpha, diameter = image.width, radius = diameter * half;
  context.globalAlpha = opacity;
  context.drawImage(image, -radius, -radius, diameter, diameter);
  context.globalAlpha = previousAlpha;
}

// node_modules/@tsparticles/canvas-utils/browser/Utils.js
var alphaMax = 255;
var alphaFactor2 = identity / alphaMax;
function drawLine(context, begin, end) {
  context.beginPath();
  context.moveTo(begin.x, begin.y);
  context.lineTo(end.x, end.y);
  context.closePath();
}
async function loadFont(font, weight) {
  try {
    await safeDocument().fonts.load(`${weight ?? "400"} 36px '${font ?? "Verdana"}'`);
  } catch {
  }
}

// node_modules/@tsparticles/shape-emoji/browser/EmojiDrawer.js
var defaultFont = '"Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif';
var noPadding = 0;
var firstItem = 0;
var EmojiDrawer = class {
  #emojiShapeDict = /* @__PURE__ */ new Map();
  destroy() {
    for (const [key, data] of this.#emojiShapeDict) {
      if (data instanceof ImageBitmap) {
        data.close();
      }
      this.#emojiShapeDict.delete(key);
    }
  }
  draw(data) {
    const key = data.particle.emojiDataKey;
    if (!key) {
      return;
    }
    const image = this.#emojiShapeDict.get(key);
    if (!image) {
      return;
    }
    drawEmoji(data, image);
  }
  async init(container) {
    const options = container.actualOptions, shapeData = options.particles.shape;
    if (!validTypes.some((t) => isInArray(t, shapeData.type))) {
      return;
    }
    const promises = [loadFont(defaultFont)], shapeOptions = validTypes.map((t) => shapeData.options[t])[firstItem];
    executeOnSingleOrMultiple(shapeOptions, (shape) => {
      if (shape.font) {
        promises.push(loadFont(shape.font));
      }
    });
    await Promise.all(promises);
  }
  particleDestroy(particle) {
    particle.emojiDataKey = void 0;
  }
  particleInit(container, particle) {
    const shapeData = particle.shapeData;
    if (!shapeData.value) {
      return;
    }
    const emoji = itemFromSingleOrMultiple(shapeData.value, particle.randomIndexData);
    if (!emoji) {
      return;
    }
    const emojiOptions = typeof emoji === "string" ? {
      font: shapeData.font ?? defaultFont,
      padding: shapeData.padding ?? noPadding,
      value: emoji
    } : __spreadValues(__spreadValues({
      font: defaultFont,
      padding: noPadding
    }, shapeData), emoji), font = emojiOptions.font, value = emojiOptions.value, cacheKey = `${value}_${font}`;
    if (this.#emojiShapeDict.has(cacheKey)) {
      particle.emojiDataKey = cacheKey;
      return;
    }
    const padding = emojiOptions.padding * double, maxSize = getRangeMax(particle.size.value), fullSize = maxSize + padding, canvasSize = fullSize * double, cacheCanvas = new OffscreenCanvas(canvasSize, canvasSize), context = cacheCanvas.getContext("2d", container.canvas.render.settings);
    if (!context) {
      return;
    }
    context.font = `400 ${(maxSize * double).toString()}px ${font}`;
    context.textBaseline = "middle";
    context.textAlign = "center";
    context.fillText(value, fullSize, fullSize);
    const image = cacheCanvas instanceof HTMLCanvasElement ? cacheCanvas : cacheCanvas.transferToImageBitmap();
    this.#emojiShapeDict.set(cacheKey, image);
    particle.emojiDataKey = cacheKey;
  }
};

// node_modules/@tsparticles/shape-emoji/browser/index.js
async function loadEmojiShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(validTypes, () => Promise.resolve(new EmojiDrawer()));
  });
}

// node_modules/@tsparticles/plugin-interactivity/browser/InteractivityPlugin.js
var InteractivityPlugin = class {
  id = "interactivity";
  #pluginManager;
  constructor(pluginManager) {
    this.#pluginManager = pluginManager;
  }
  async getPlugin(container) {
    const { InteractivityPluginInstance } = await import("./InteractivityPluginInstance-PZUCFQIO.js");
    return new InteractivityPluginInstance(this.#pluginManager, container);
  }
  loadOptions(container, options, source) {
    if (!this.needsPlugin()) {
      return;
    }
    let interactivityOptions = options.interactivity;
    if (!interactivityOptions?.load) {
      options.interactivity = interactivityOptions = new Interactivity(this.#pluginManager, container);
    }
    interactivityOptions.load(source?.interactivity);
    const interactors = this.#pluginManager.interactors?.get(container);
    if (!interactors) {
      return;
    }
    for (const interactor of interactors) {
      if (interactor.loadOptions) {
        interactor.loadOptions(options, source);
      }
    }
  }
  loadParticlesOptions(container, options, source) {
    if (source?.interactivity) {
      options.interactivity = deepExtend({}, source.interactivity);
    }
    const interactors = this.#pluginManager.interactors?.get(container);
    if (!interactors) {
      return;
    }
    for (const interactor of interactors) {
      interactor.loadParticlesOptions?.(options, source);
    }
  }
  needsPlugin() {
    return true;
  }
};

// node_modules/@tsparticles/plugin-interactivity/browser/BaseClasses/ExternalInteractorBase.js
var ExternalInteractorBase = class {
  type = InteractorType.external;
  container;
  constructor(container) {
    this.container = container;
  }
};

// node_modules/@tsparticles/plugin-interactivity/browser/BaseClasses/ParticlesInteractorBase.js
var ParticlesInteractorBase = class {
  type = InteractorType.particles;
  container;
  constructor(container) {
    this.container = container;
  }
};

// node_modules/@tsparticles/plugin-interactivity/browser/utils.js
function findItemFromSingleOrMultiple(obj, callback) {
  if (isArray(obj)) {
    return obj.find((t, index) => callback(t, index));
  }
  const defaultIndex = 0;
  return callback(obj, defaultIndex) ? obj : void 0;
}
function checkSelector(element, selectors) {
  const res = executeOnSingleOrMultiple(selectors, (selector) => {
    return element.matches(selector);
  });
  return isArray(res) ? res.some((t) => t) : res;
}
function isDivModeEnabled(mode, divs) {
  return !!findItemFromSingleOrMultiple(divs, (t) => t.enable && isInArray(mode, t.mode));
}
function divModeExecute(mode, divs, callback) {
  executeOnSingleOrMultiple(divs, (div) => {
    const divMode2 = div.mode, divEnabled = div.enable;
    if (divEnabled && isInArray(mode, divMode2)) {
      singleDivModeExecute(div, callback);
    }
  });
}
function singleDivModeExecute(div, callback) {
  const selectors = div.selectors;
  executeOnSingleOrMultiple(selectors, (selector) => {
    callback(selector, div);
  });
}
function divMode(divs, element) {
  if (!element || !divs) {
    return;
  }
  return findItemFromSingleOrMultiple(divs, (div) => {
    return checkSelector(element, div.selectors);
  });
}

// node_modules/@tsparticles/plugin-interactivity/browser/index.js
async function loadInteractivityPlugin(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    const interactivityEngine = e, interactivityPluginManager = interactivityEngine.pluginManager;
    interactivityPluginManager.addPlugin(new InteractivityPlugin(interactivityPluginManager));
    interactivityPluginManager.initializers.interactors ??= /* @__PURE__ */ new Map();
    interactivityPluginManager.interactors ??= /* @__PURE__ */ new Map();
    interactivityPluginManager.addInteractor = (name, interactorInitializer) => {
      interactivityPluginManager.initializers.interactors ??= /* @__PURE__ */ new Map();
      interactivityPluginManager.initializers.interactors.set(name, interactorInitializer);
    };
    interactivityPluginManager.getInteractors = async (container, force = false) => {
      interactivityPluginManager.interactors ??= /* @__PURE__ */ new Map();
      interactivityPluginManager.initializers.interactors ??= /* @__PURE__ */ new Map();
      return getItemsFromInitializer(container, interactivityPluginManager.interactors, interactivityPluginManager.initializers.interactors, force);
    };
    interactivityPluginManager.setOnClickHandler = (callback) => {
      const { items } = interactivityEngine;
      if (!items.length) {
        throw new Error("Click handlers can only be set after calling tsParticles.load()");
      }
      items.forEach((item) => {
        const interactivityContainer = item;
        interactivityContainer.addClickHandler?.(callback);
      });
    };
  });
}
function ensureInteractivityPluginLoaded(e) {
  if (!e.pluginManager.addInteractor) {
    throw new Error("tsParticles Interactivity Plugin is not loaded");
  }
}

// node_modules/@tsparticles/interaction-external-attract/browser/Utils.js
var minFactor = 1;
var minRadius2 = 0;
var updateVector2 = Vector.origin;
function processAttract(pluginManager, container, position, attractRadius, area, queryCb, onAttractParticle) {
  const attractOptions = container.actualOptions.interactivity?.modes.attract;
  if (!attractOptions) {
    return;
  }
  const query = container.particles.grid.query(area, queryCb);
  for (const particle of query) {
    const { dx, dy, distance } = getDistances(particle.position, position), velocity = attractOptions.speed * attractOptions.factor, attractFactor2 = clamp(pluginManager.getEasing(attractOptions.easing)(identity - distance / attractRadius) * velocity, minFactor, attractOptions.maxSpeed);
    updateVector2.x = !distance ? velocity : dx / distance * attractFactor2;
    updateVector2.y = !distance ? velocity : dy / distance * attractFactor2;
    onAttractParticle?.(particle);
    particle.position.subFrom(updateVector2);
  }
}
function clickAttract(pluginManager, container, interactivityData, enabledCb, onAttractParticle) {
  container.attract ??= { particles: [] };
  const { attract } = container;
  if (!attract.finish) {
    attract.count ??= 0;
    attract.count++;
    if (attract.count === container.particles.count) {
      attract.finish = true;
    }
  }
  if (attract.clicking) {
    const mousePos = interactivityData.mouse.clickPosition, attractRadius = container.retina.attractModeDistance;
    if (!attractRadius || attractRadius < minRadius2 || !mousePos) {
      return;
    }
    processAttract(pluginManager, container, mousePos, attractRadius, new Circle(mousePos.x, mousePos.y, attractRadius), (p) => enabledCb(p), onAttractParticle);
  } else if (attract.clicking === false) {
    attract.particles = [];
  }
}
function hoverAttract(pluginManager, container, interactivityData, enabledCb, onAttractParticle) {
  const mousePos = interactivityData.mouse.position, attractRadius = container.retina.attractModeDistance;
  if (!attractRadius || attractRadius < minRadius2 || !mousePos) {
    return;
  }
  processAttract(pluginManager, container, mousePos, attractRadius, new Circle(mousePos.x, mousePos.y, attractRadius), (p) => enabledCb(p), onAttractParticle);
}

// node_modules/@tsparticles/interaction-external-attract/browser/Options/Classes/Attract.js
var Attract = class {
  distance = 200;
  duration = 0.4;
  easing = "ease-out-quad";
  factor = 1;
  maxSpeed = 50;
  restore;
  speed = 1;
  constructor() {
    this.restore = {
      enable: false,
      delay: 0,
      speed: 0.08,
      follow: true
    };
  }
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
    loadProperty(this, "duration", data.duration);
    if (data.easing !== void 0) {
      this.easing = data.easing;
    }
    loadProperty(this, "factor", data.factor);
    if (data.maxSpeed !== void 0) {
      this.maxSpeed = data.maxSpeed;
    }
    loadProperty(this, "speed", data.speed);
    if (data.restore !== void 0) {
      this.restore.enable = data.restore.enable ?? this.restore.enable;
      this.restore.delay = data.restore.delay ?? this.restore.delay;
      this.restore.speed = data.restore.speed ?? this.restore.speed;
      this.restore.follow = data.restore.follow ?? this.restore.follow;
    }
  }
};

// node_modules/@tsparticles/interaction-external-attract/browser/Attractor.js
var attractMode = "attract";
var minVelocityLengthSq = 0;
var minRestoreSpeed = 1e-3;
var maxRestoreSpeed = 1;
var restoreEpsilon = 0.5;
var Attractor = class extends ExternalInteractorBase {
  handleClickMode;
  #interactedThisFrame;
  #maxDistance;
  #pluginManager;
  #restoreData;
  constructor(pluginManager, container) {
    super(container);
    this.#pluginManager = pluginManager;
    this.#maxDistance = 0;
    this.#interactedThisFrame = /* @__PURE__ */ new Set();
    this.#restoreData = /* @__PURE__ */ new Map();
    container.attract ??= { particles: [] };
    this.handleClickMode = (mode, interactivityData) => {
      const options = this.container.actualOptions, attract = options.interactivity?.modes.attract;
      if (!attract || mode !== attractMode) {
        return;
      }
      container.attract ??= { particles: [] };
      container.attract.clicking = true;
      container.attract.count = 0;
      for (const particle of container.attract.particles) {
        if (!this.isEnabled(interactivityData, particle)) {
          continue;
        }
        particle.velocity.setTo(particle.initialVelocity);
      }
      container.attract.particles = [];
      container.attract.finish = false;
      setTimeout(() => {
        if (container.destroyed) {
          return;
        }
        container.attract ??= { particles: [] };
        container.attract.clicking = false;
      }, attract.duration * millisecondsToSeconds);
    };
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    const container = this.container, attract = container.actualOptions.interactivity?.modes.attract;
    if (!attract) {
      return;
    }
    this.#maxDistance = attract.distance;
    container.retina.attractModeDistance = attract.distance * container.retina.pixelRatio;
  }
  interact(interactivityData) {
    this.#interactedThisFrame.clear();
    const container = this.container, options = container.actualOptions, mouseMoveStatus = interactivityData.status === mouseMoveEvent, events = options.interactivity?.events;
    if (!events) {
      return;
    }
    const { enable: hoverEnabled, mode: hoverMode } = events.onHover, { enable: clickEnabled, mode: clickMode } = events.onClick;
    if (mouseMoveStatus && hoverEnabled && isInArray(attractMode, hoverMode)) {
      hoverAttract(this.#pluginManager, this.container, interactivityData, (p) => this.isEnabled(interactivityData, p), (p) => {
        this.#trackInteractedParticle(p);
      });
    } else if (clickEnabled && isInArray(attractMode, clickMode)) {
      clickAttract(this.#pluginManager, this.container, interactivityData, (p) => this.isEnabled(interactivityData, p), (p) => {
        this.#trackInteractedParticle(p);
      });
    }
    this.#restoreParticles();
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    if ((!mouse.position || !events?.onHover.enable) && (!mouse.clickPosition || !events?.onClick.enable)) {
      return false;
    }
    const hoverMode = events.onHover.mode, clickMode = events.onClick.mode;
    return isInArray(attractMode, hoverMode) || isInArray(attractMode, clickMode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "attract", Attract, ...sources);
  }
  reset() {
  }
  #restoreParticles() {
    const restore = this.container.actualOptions.interactivity?.modes.attract?.restore;
    if (!restore?.enable || !this.#restoreData.size) {
      return;
    }
    const now = Date.now(), restoreDelay = restore.delay * millisecondsToSeconds, restoreSpeed = Math.max(minRestoreSpeed, Math.min(maxRestoreSpeed, restore.speed));
    for (const [particle, restoreData] of this.#restoreData) {
      if (this.#interactedThisFrame.has(particle)) {
        continue;
      }
      if (particle.destroyed) {
        this.#restoreData.delete(particle);
        continue;
      }
      const target = restoreData.target;
      if (now - restoreData.lastInteractionTime < restoreDelay) {
        continue;
      }
      let dx = target.x - particle.position.x, dy = target.y - particle.position.y, dz = target.z - particle.position.z;
      if (restore.follow && particle.options.move.enable) {
        const { x: vx, y: vy, z: vz } = particle.velocity, velocityLengthSq = vx * vx + vy * vy + vz * vz;
        if (velocityLengthSq > minVelocityLengthSq) {
          const parallelScale = (dx * vx + dy * vy + dz * vz) / velocityLengthSq;
          dx -= vx * parallelScale;
          dy -= vy * parallelScale;
          dz -= vz * parallelScale;
        }
      }
      particle.position.x += dx * restoreSpeed;
      particle.position.y += dy * restoreSpeed;
      particle.position.z += dz * restoreSpeed;
      if (Math.abs(dx) <= restoreEpsilon && Math.abs(dy) <= restoreEpsilon) {
        particle.position.x = target.x;
        particle.position.y = target.y;
        particle.position.z = target.z;
        this.#restoreData.delete(particle);
        continue;
      }
    }
  }
  #trackInteractedParticle(particle) {
    this.#interactedThisFrame.add(particle);
    const restore = this.container.actualOptions.interactivity?.modes.attract?.restore;
    if (!restore?.enable) {
      return;
    }
    const now = Date.now();
    let restoreData = this.#restoreData.get(particle);
    if (!restoreData) {
      restoreData = {
        target: particle.position.copy(),
        lastInteractionTime: now
      };
      this.#restoreData.set(particle, restoreData);
    }
    restoreData.lastInteractionTime = now;
  }
};

// node_modules/@tsparticles/interaction-external-attract/browser/index.js
async function loadExternalAttractInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalAttract", (container) => {
      return Promise.resolve(new Attractor(e.pluginManager, container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-bounce/browser/Utils.js
var halfPI = Math.PI * half;
var toleranceFactor = 10;
function processBounce(container, position, radius, area, enabledCb) {
  const query = container.particles.grid.query(area, enabledCb);
  for (const particle of query) {
    if (area instanceof Circle) {
      circleBounce(circleBounceDataFromParticle(particle), {
        position,
        radius,
        mass: radius ** squareExp * halfPI,
        velocity: Vector.origin,
        factor: Vector.origin
      });
    } else if (area instanceof Rectangle) {
      rectBounce(particle, calculateBounds(position, radius));
    }
  }
}
function singleSelectorBounce(container, selector, div, bounceCb) {
  const query = safeDocument().querySelectorAll(selector);
  if (!query.length) {
    return;
  }
  query.forEach((item) => {
    const elem = item, pxRatio = container.retina.pixelRatio, pos = {
      x: (elem.offsetLeft + elem.offsetWidth * half) * pxRatio,
      y: (elem.offsetTop + elem.offsetHeight * half) * pxRatio
    }, radius = elem.offsetWidth * half * pxRatio, tolerance = toleranceFactor * pxRatio, area = div.type === DivType.circle ? new Circle(pos.x, pos.y, radius + tolerance) : new Rectangle(elem.offsetLeft * pxRatio - tolerance, elem.offsetTop * pxRatio - tolerance, elem.offsetWidth * pxRatio + tolerance * double, elem.offsetHeight * pxRatio + tolerance * double);
    bounceCb(pos, radius, area);
  });
}
function divBounce(container, divs, bounceMode2, enabledCb) {
  divModeExecute(bounceMode2, divs, (selector, div) => {
    singleSelectorBounce(container, selector, div, (pos, radius, area) => {
      processBounce(container, pos, radius, area, enabledCb);
    });
  });
}
function mouseBounce(container, interactivityData, enabledCb) {
  const pxRatio = container.retina.pixelRatio, tolerance = toleranceFactor * pxRatio, mousePos = interactivityData.mouse.position, radius = container.retina.bounceModeDistance;
  if (!radius || radius < minRadius || !mousePos) {
    return;
  }
  processBounce(container, mousePos, radius, new Circle(mousePos.x, mousePos.y, radius + tolerance), enabledCb);
}
function rectSideBounce(data) {
  const res = { bounced: false }, { pSide, pOtherSide, rectSide, rectOtherSide, velocity, factor } = data;
  if (pOtherSide.min < rectOtherSide.min || pOtherSide.min > rectOtherSide.max || pOtherSide.max < rectOtherSide.min || pOtherSide.max > rectOtherSide.max) {
    return res;
  }
  if (pSide.max >= rectSide.min && pSide.max <= (rectSide.max + rectSide.min) * half && velocity > minVelocity || pSide.min <= rectSide.max && pSide.min > (rectSide.max + rectSide.min) * half && velocity < minVelocity) {
    res.velocity = velocity * -factor;
    res.bounced = true;
  }
  return res;
}
function rectBounce(particle, divBounds) {
  const pPos = particle.getPosition(), size = particle.getRadius(), bounds = calculateBounds(pPos, size), bounceOptions = particle.options.bounce, resH = rectSideBounce({
    pSide: {
      min: bounds.left,
      max: bounds.right
    },
    pOtherSide: {
      min: bounds.top,
      max: bounds.bottom
    },
    rectSide: {
      min: divBounds.left,
      max: divBounds.right
    },
    rectOtherSide: {
      min: divBounds.top,
      max: divBounds.bottom
    },
    velocity: particle.velocity.x,
    factor: getRangeValue(bounceOptions.horizontal.value)
  });
  if (resH.bounced) {
    if (resH.velocity !== void 0) {
      particle.velocity.x = resH.velocity;
    }
    if (resH.position !== void 0) {
      particle.position.x = resH.position;
    }
  }
  const resV = rectSideBounce({
    pSide: {
      min: bounds.top,
      max: bounds.bottom
    },
    pOtherSide: {
      min: bounds.left,
      max: bounds.right
    },
    rectSide: {
      min: divBounds.top,
      max: divBounds.bottom
    },
    rectOtherSide: {
      min: divBounds.left,
      max: divBounds.right
    },
    velocity: particle.velocity.y,
    factor: getRangeValue(bounceOptions.vertical.value)
  });
  if (resV.bounced) {
    if (resV.velocity !== void 0) {
      particle.velocity.y = resV.velocity;
    }
    if (resV.position !== void 0) {
      particle.position.y = resV.position;
    }
  }
}

// node_modules/@tsparticles/interaction-external-bounce/browser/Options/Classes/Bounce.js
var Bounce = class {
  distance = 200;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
  }
};

// node_modules/@tsparticles/interaction-external-bounce/browser/Bouncer.js
var bounceMode = "bounce";
var Bouncer = class extends ExternalInteractorBase {
  #maxDistance;
  constructor(container) {
    super(container);
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    const container = this.container, bounce2 = container.actualOptions.interactivity?.modes.bounce;
    if (!bounce2) {
      return;
    }
    this.#maxDistance = bounce2.distance;
    container.retina.bounceModeDistance = bounce2.distance * container.retina.pixelRatio;
  }
  interact(interactivityData) {
    const container = this.container, options = container.actualOptions, events = options.interactivity?.events, mouseMoveStatus = interactivityData.status === mouseMoveEvent;
    if (!events) {
      return;
    }
    const hoverEnabled = events.onHover.enable, hoverMode = events.onHover.mode, divs = events.onDiv;
    if (mouseMoveStatus && hoverEnabled && isInArray(bounceMode, hoverMode)) {
      mouseBounce(this.container, interactivityData, (p) => this.isEnabled(interactivityData, p));
    } else {
      divBounce(this.container, divs, bounceMode, (p) => this.isEnabled(interactivityData, p));
    }
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    if (!events) {
      return false;
    }
    const divs = events.onDiv;
    return !!mouse.position && events.onHover.enable && isInArray(bounceMode, events.onHover.mode) || isDivModeEnabled(bounceMode, divs);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "bounce", Bounce, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-bounce/browser/index.js
async function loadExternalBounceInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalBounce", (container) => {
      return Promise.resolve(new Bouncer(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-bubble/browser/Options/Classes/BubbleBase.js
var BubbleBase = class {
  color;
  distance = 200;
  duration = 0.4;
  mix = false;
  opacity;
  size;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
    loadProperty(this, "duration", data.duration);
    loadProperty(this, "mix", data.mix);
    loadRangeProperty(this, "opacity", data.opacity);
    if (data.color !== void 0) {
      const sourceColor = isArray(this.color) ? void 0 : this.color;
      this.color = executeOnSingleOrMultiple(data.color, (color) => {
        return OptionsColor.create(sourceColor, color);
      });
    }
    loadProperty(this, "size", data.size);
  }
};

// node_modules/@tsparticles/interaction-external-bubble/browser/Options/Classes/BubbleDiv.js
var BubbleDiv = class extends BubbleBase {
  selectors = [];
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "selectors", data.selectors);
  }
};

// node_modules/@tsparticles/interaction-external-bubble/browser/Options/Classes/Bubble.js
var Bubble = class extends BubbleBase {
  divs;
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    this.divs = executeOnSingleOrMultiple(data.divs, (div) => {
      const tmp = new BubbleDiv();
      tmp.load(div);
      return tmp;
    });
  }
};

// node_modules/@tsparticles/interaction-external-bubble/browser/BubbleModifier.js
var BubbleModifier = class {
  div;
  enabled = false;
  fillColor;
  finalColor;
  id = "bubble";
  inRange = false;
  opacity;
  priority = 100;
  radius;
  strokeColor;
};

// node_modules/@tsparticles/interaction-external-bubble/browser/Enums.js
var ProcessBubbleType;
(function(ProcessBubbleType2) {
  ProcessBubbleType2["color"] = "color";
  ProcessBubbleType2["opacity"] = "opacity";
  ProcessBubbleType2["size"] = "size";
})(ProcessBubbleType || (ProcessBubbleType = {}));

// node_modules/@tsparticles/interaction-external-bubble/browser/Utils.js
function calculateBubbleValue(particleValue, modeValue, optionsValue, ratio) {
  if (modeValue >= optionsValue) {
    const value = particleValue + (modeValue - optionsValue) * ratio;
    return clamp(value, particleValue, modeValue);
  } else if (modeValue < optionsValue) {
    const value = particleValue - (optionsValue - modeValue) * ratio;
    return clamp(value, modeValue, particleValue);
  }
  return void 0;
}

// node_modules/@tsparticles/interaction-external-bubble/browser/Bubbler.js
var bubbleMode = "bubble";
var minDistance2 = 0;
var defaultClickTime = 0;
var defaultOpacity2 = 1;
var ratioOffset = 1;
var defaultBubbleValue = 0;
var minRatio = 0;
var defaultRatio2 = 1;
var Bubbler = class extends ExternalInteractorBase {
  handleClickMode;
  #maxDistance;
  #modifiers = /* @__PURE__ */ new WeakMap();
  #pluginManager;
  constructor(pluginManager, container) {
    super(container);
    this.#pluginManager = pluginManager;
    this.#maxDistance = 0;
    container.bubble ??= {};
    this.handleClickMode = (mode) => {
      if (mode !== bubbleMode) {
        return;
      }
      container.bubble ??= {};
      container.bubble.clicking = true;
    };
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear(particle, _delta, force) {
    const mod = this.#modifiers.get(particle);
    if (mod?.inRange && !force) {
      return;
    }
    particle.removeModifier(bubbleMode);
    this.#modifiers.delete(particle);
  }
  getOrCreateModifier(particle) {
    let mod = this.#modifiers.get(particle);
    if (!mod) {
      mod = new BubbleModifier();
      this.#modifiers.set(particle, mod);
      particle.addModifier(mod);
    }
    return mod;
  }
  init() {
    const container = this.container, bubble = container.actualOptions.interactivity?.modes.bubble;
    if (!bubble) {
      return;
    }
    this.#maxDistance = bubble.distance;
    container.retina.bubbleModeDistance = bubble.distance * container.retina.pixelRatio;
    if (bubble.size !== void 0) {
      container.retina.bubbleModeSize = bubble.size * container.retina.pixelRatio;
    }
  }
  interact(interactivityData, delta) {
    const options = this.container.actualOptions, events = options.interactivity?.events;
    if (!events) {
      return;
    }
    const onHover = events.onHover, onClick = events.onClick, hoverEnabled = onHover.enable, hoverMode = onHover.mode, clickEnabled = onClick.enable, clickMode = onClick.mode, divs = events.onDiv;
    if (hoverEnabled && isInArray(bubbleMode, hoverMode)) {
      this.#hoverBubble(interactivityData);
    } else if (clickEnabled && isInArray(bubbleMode, clickMode)) {
      this.#clickBubble(interactivityData);
    } else {
      divModeExecute(bubbleMode, divs, (selector, div) => {
        this.#singleSelectorHover(interactivityData, delta, selector, div);
      });
    }
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    if (!events) {
      return false;
    }
    const { onClick, onDiv, onHover } = events, divBubble = isDivModeEnabled(bubbleMode, onDiv);
    if (!(divBubble || onHover.enable && !!mouse.position || onClick.enable && mouse.clickPosition)) {
      return false;
    }
    return isInArray(bubbleMode, onHover.mode) || isInArray(bubbleMode, onClick.mode) || divBubble;
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "bubble", Bubble, ...sources);
  }
  reset(_interactivityData, particle) {
    const mod = this.#modifiers.get(particle);
    if (mod) {
      mod.enabled = false;
      mod.inRange = false;
    }
  }
  #clickBubble(interactivityData) {
    const container = this.container, options = container.actualOptions, mouseClickPos = interactivityData.mouse.clickPosition, bubbleOptions = options.interactivity?.modes.bubble;
    if (!bubbleOptions || !mouseClickPos) {
      return;
    }
    container.bubble ??= {};
    const distance = container.retina.bubbleModeDistance;
    if (!distance || distance < minDistance2) {
      return;
    }
    const query = container.particles.grid.queryCircle(mouseClickPos, distance, (p) => this.isEnabled(interactivityData, p)), { bubble } = container;
    for (const particle of query) {
      if (!bubble.clicking) {
        continue;
      }
      const mod = this.getOrCreateModifier(particle);
      mod.enabled = !bubble.durationEnd;
      mod.inRange = !bubble.durationEnd;
      const pos = particle.getPosition(), distMouse = getDistance(pos, mouseClickPos), timeSpent = (performance.now() - (interactivityData.mouse.clickTime ?? defaultClickTime)) / millisecondsToSeconds;
      if (timeSpent > bubbleOptions.duration) {
        bubble.durationEnd = true;
      }
      if (timeSpent > bubbleOptions.duration * double) {
        bubble.clicking = false;
        bubble.durationEnd = false;
      }
      const sizeData = {
        bubbleObj: {
          optValue: container.retina.bubbleModeSize,
          value: mod.radius
        },
        particlesObj: {
          optValue: particle.size.max,
          value: particle.size.value
        },
        type: ProcessBubbleType.size
      };
      this.#process(particle, distMouse, timeSpent, sizeData);
      const opacityData = {
        bubbleObj: {
          optValue: bubbleOptions.opacity,
          value: mod.opacity
        },
        particlesObj: {
          optValue: particle.opacity?.max ?? defaultOpacity2,
          value: particle.opacity?.value ?? defaultOpacity2
        },
        type: ProcessBubbleType.opacity
      };
      this.#process(particle, distMouse, timeSpent, opacityData);
      if (!bubble.durationEnd && distMouse <= distance) {
        this.#hoverBubbleColor(particle, distMouse);
      } else {
        mod.fillColor = void 0;
        mod.strokeColor = void 0;
      }
    }
  }
  #hoverBubble(interactivityData) {
    const container = this.container, mousePos = interactivityData.mouse.position, distance = container.retina.bubbleModeDistance;
    if (!distance || distance < minDistance2 || !mousePos) {
      return;
    }
    const query = container.particles.grid.queryCircle(mousePos, distance, (p) => this.isEnabled(interactivityData, p));
    for (const particle of query) {
      const mod = this.getOrCreateModifier(particle);
      mod.enabled = true;
      mod.inRange = true;
      const pos = particle.getPosition(), pointDistance = getDistance(pos, mousePos), ratio = ratioOffset - pointDistance / distance;
      if (pointDistance <= distance) {
        if (ratio >= minRatio && interactivityData.status === mouseMoveEvent) {
          this.#hoverBubbleSize(particle, ratio);
          this.#hoverBubbleOpacity(particle, ratio);
          this.#hoverBubbleColor(particle, ratio);
        }
      } else {
        this.reset(interactivityData, particle);
      }
      if (interactivityData.status === mouseLeaveEvent) {
        this.reset(interactivityData, particle);
      }
    }
  }
  #hoverBubbleColor(particle, ratio, divBubble) {
    const options = this.container.actualOptions, bubbleOptions = divBubble ?? options.interactivity?.modes.bubble, mod = this.getOrCreateModifier(particle);
    if (!bubbleOptions) {
      return;
    }
    if (!mod.finalColor) {
      const modeColor = bubbleOptions.color;
      if (!modeColor) {
        return;
      }
      const bubbleColor = itemFromSingleOrMultiple(modeColor);
      mod.finalColor = rangeColorToHsl(this.#pluginManager, bubbleColor);
    }
    if (!mod.finalColor) {
      return;
    }
    if (bubbleOptions.mix) {
      mod.fillColor = void 0;
      mod.strokeColor = void 0;
      const pColor = particle.getFillColor();
      if (pColor) {
        const mixedColor = rgbToHsl(colorMix(pColor, mod.finalColor, ratioOffset - ratio, ratio));
        mod.fillColor = mixedColor;
        mod.strokeColor = mixedColor;
      } else {
        mod.fillColor = mod.finalColor;
        mod.strokeColor = mod.finalColor;
      }
    } else {
      mod.fillColor = mod.finalColor;
      mod.strokeColor = mod.finalColor;
    }
  }
  #hoverBubbleOpacity(particle, ratio, divBubble) {
    const container = this.container, options = container.actualOptions, modeOpacity = divBubble?.opacity ?? options.interactivity?.modes.bubble?.opacity;
    if (!modeOpacity) {
      return;
    }
    const pOpacity = particle.opacity?.value ?? defaultOpacity2, opacity = calculateBubbleValue(pOpacity, modeOpacity, particle.opacity?.max ?? defaultOpacity2, ratio);
    if (opacity !== void 0) {
      const mod = this.getOrCreateModifier(particle);
      mod.opacity = opacity;
    }
  }
  #hoverBubbleSize(particle, ratio, divBubble) {
    const container = this.container, modeSize = divBubble?.size ? divBubble.size * container.retina.pixelRatio : container.retina.bubbleModeSize;
    if (modeSize === void 0) {
      return;
    }
    const pSize = particle.size.value, size = calculateBubbleValue(pSize, modeSize, particle.size.max, ratio);
    if (size !== void 0) {
      const mod = this.getOrCreateModifier(particle);
      mod.radius = size;
    }
  }
  #process(particle, distMouse, timeSpent, data) {
    const container = this.container, bubbleParam = data.bubbleObj.optValue, options = container.actualOptions, bubbleOptions = options.interactivity?.modes.bubble;
    if (!bubbleOptions || bubbleParam === void 0) {
      return;
    }
    const bubbleDuration = bubbleOptions.duration, bubbleDistance = container.retina.bubbleModeDistance, particlesParam = data.particlesObj.optValue, pObjBubble = data.bubbleObj.value, pObj = data.particlesObj.value ?? defaultBubbleValue, type = data.type;
    if (!bubbleDistance || bubbleDistance < minDistance2 || bubbleParam === particlesParam) {
      return;
    }
    container.bubble ??= {};
    const mod = this.getOrCreateModifier(particle);
    if (container.bubble.durationEnd) {
      if (pObjBubble) {
        if (type === ProcessBubbleType.size) {
          mod.radius = void 0;
        }
        if (type === ProcessBubbleType.opacity) {
          mod.opacity = void 0;
        }
      }
    } else {
      if (distMouse <= bubbleDistance) {
        const obj = pObjBubble ?? pObj;
        if (obj !== bubbleParam) {
          const value = pObj - timeSpent * (pObj - bubbleParam) / bubbleDuration;
          if (type === ProcessBubbleType.size) {
            mod.radius = value;
          }
          if (type === ProcessBubbleType.opacity) {
            mod.opacity = value;
          }
        }
      } else {
        if (type === ProcessBubbleType.size) {
          mod.radius = void 0;
        }
        if (type === ProcessBubbleType.opacity) {
          mod.opacity = void 0;
        }
      }
    }
  }
  #singleSelectorHover(interactivityData, delta, selector, div) {
    const container = this.container, selectors = safeDocument().querySelectorAll(selector), bubble = container.actualOptions.interactivity?.modes.bubble;
    if (!bubble || !selectors.length) {
      return;
    }
    selectors.forEach((item) => {
      const elem = item, pxRatio = container.retina.pixelRatio, pos = {
        x: (elem.offsetLeft + elem.offsetWidth * half) * pxRatio,
        y: (elem.offsetTop + elem.offsetHeight * half) * pxRatio
      }, repulseRadius = elem.offsetWidth * half * pxRatio, area = div.type === DivType.circle ? new Circle(pos.x, pos.y, repulseRadius) : new Rectangle(elem.offsetLeft * pxRatio, elem.offsetTop * pxRatio, elem.offsetWidth * pxRatio, elem.offsetHeight * pxRatio), query = container.particles.grid.query(area, (p) => this.isEnabled(interactivityData, p));
      for (const particle of query) {
        if (!area.contains(particle.getPosition())) {
          continue;
        }
        const mod = this.getOrCreateModifier(particle);
        mod.enabled = true;
        mod.inRange = true;
        const divs = bubble.divs, divBubble = divMode(divs, elem);
        if (!mod.div || mod.div !== elem) {
          this.clear(particle, delta, true);
          mod.div = elem;
        }
        this.#hoverBubbleSize(particle, defaultRatio2, divBubble);
        this.#hoverBubbleOpacity(particle, defaultRatio2, divBubble);
        this.#hoverBubbleColor(particle, defaultRatio2, divBubble);
      }
    });
  }
};

// node_modules/@tsparticles/interaction-external-bubble/browser/index.js
async function loadExternalBubbleInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalBubble", (container) => {
      return Promise.resolve(new Bubbler(e.pluginManager, container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-connect/browser/Options/Classes/ConnectLinks.js
var ConnectLinks = class {
  opacity = 0.5;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadRangeProperty(this, "opacity", data.opacity);
  }
};

// node_modules/@tsparticles/interaction-external-connect/browser/Options/Classes/Connect.js
var Connect = class {
  distance = 80;
  links = new ConnectLinks();
  radius = 60;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
    this.links.load(data.links);
    loadProperty(this, "radius", data.radius);
  }
};

// node_modules/@tsparticles/interaction-external-connect/browser/Utils.js
var gradientMin = 0;
var gradientMax = 1;
var defaultLinksWidth = 0;
function gradient(container, context, p1, p2, opacity) {
  const gradStop = Math.floor(p2.getRadius() / p1.getRadius()), color1 = p1.getFillColor(), color2 = p2.getFillColor();
  if (!color1 || !color2) {
    return;
  }
  const sourcePos = p1.getPosition(), destPos = p2.getPosition(), midRgb = colorMix(color1, color2, p1.getRadius(), p2.getRadius()), grad = context.createLinearGradient(sourcePos.x, sourcePos.y, destPos.x, destPos.y);
  grad.addColorStop(gradientMin, getStyleFromHsl(color1, container.hdr, opacity));
  grad.addColorStop(clamp(gradStop, gradientMin, gradientMax), getStyleFromRgb(midRgb, container.hdr, opacity));
  grad.addColorStop(gradientMax, getStyleFromHsl(color2, container.hdr, opacity));
  return grad;
}
function drawConnectLine(context, width, lineStyle2, begin, end) {
  drawLine(context, begin, end);
  context.lineWidth = width;
  context.strokeStyle = lineStyle2;
  context.stroke();
}
function lineStyle(container, ctx, p1, p2) {
  const options = container.actualOptions, connectOptions = options.interactivity?.modes.connect;
  if (!connectOptions) {
    return;
  }
  return gradient(container, ctx, p1, p2, connectOptions.links.opacity);
}
function drawConnection(container, p1, p2) {
  container.canvas.render.draw((ctx) => {
    const ls = lineStyle(container, ctx, p1, p2);
    if (!ls) {
      return;
    }
    const pos1 = p1.getPosition(), pos2 = p2.getPosition();
    drawConnectLine(ctx, p1.retina.linksWidth ?? defaultLinksWidth, ls, pos1, pos2);
  });
}

// node_modules/@tsparticles/interaction-external-connect/browser/Connector.js
var connectMode = "connect";
var minDistance3 = 0;
var Connector = class extends ExternalInteractorBase {
  #maxDistance;
  constructor(container) {
    super(container);
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    const container = this.container, connect = container.actualOptions.interactivity?.modes.connect;
    if (!connect) {
      return;
    }
    this.#maxDistance = connect.distance;
    container.retina.connectModeDistance = connect.distance * container.retina.pixelRatio;
    container.retina.connectModeRadius = connect.radius * container.retina.pixelRatio;
  }
  interact(interactivityData) {
    const container = this.container, options = container.actualOptions;
    if (options.interactivity?.events.onHover.enable && interactivityData.status === "pointermove") {
      const mousePos = interactivityData.mouse.position, { connectModeDistance, connectModeRadius } = container.retina;
      if (!connectModeDistance || connectModeDistance < minDistance3 || !connectModeRadius || connectModeRadius < minDistance3 || !mousePos) {
        return;
      }
      const distance = Math.abs(connectModeRadius), query = container.particles.grid.queryCircle(mousePos, distance, (p) => this.isEnabled(interactivityData, p));
      query.forEach((p1, i) => {
        const pos1 = p1.getPosition(), indexOffset = 1;
        for (const p2 of query.slice(i + indexOffset)) {
          const pos2 = p2.getPosition(), distMax = Math.abs(connectModeDistance), xDiff = Math.abs(pos1.x - pos2.x), yDiff = Math.abs(pos1.y - pos2.y);
          if (xDiff < distMax && yDiff < distMax) {
            drawConnection(container, p1, p2);
          }
        }
      });
    }
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, mouse = interactivityData.mouse, events = (particle?.interactivity ?? container.actualOptions.interactivity)?.events;
    if (!(events?.onHover.enable && mouse.position)) {
      return false;
    }
    return isInArray(connectMode, events.onHover.mode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "connect", Connect, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-connect/browser/index.js
async function loadExternalConnectInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalConnect", (container) => {
      return Promise.resolve(new Connector(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-destroy/browser/Utils.js
var toleranceFactor2 = 10;
function processDestroy(container, area) {
  const query = container.particles.grid.query(area);
  for (const particle of query) {
    particle.destroy();
  }
}
function singleSelectorDestroy(container, selector, div) {
  const query = safeDocument().querySelectorAll(selector);
  if (!query.length) {
    return;
  }
  query.forEach((item) => {
    const elem = item, pxRatio = container.retina.pixelRatio, pos = {
      x: (elem.offsetLeft + elem.offsetWidth * half) * pxRatio,
      y: (elem.offsetTop + elem.offsetHeight * half) * pxRatio
    }, radius = elem.offsetWidth * half * pxRatio, tolerance = toleranceFactor2 * pxRatio, area = div.type === DivType.circle ? new Circle(pos.x, pos.y, radius + tolerance) : new Rectangle(elem.offsetLeft * pxRatio - tolerance, elem.offsetTop * pxRatio - tolerance, elem.offsetWidth * pxRatio + tolerance * double, elem.offsetHeight * pxRatio + tolerance * double);
    processDestroy(container, area);
  });
}
function divDestroy(container, divs, destroyMode2) {
  divModeExecute(destroyMode2, divs, (selector, div) => {
    singleSelectorDestroy(container, selector, div);
  });
}
function mouseDestroy(container, interactivityData) {
  const pxRatio = container.retina.pixelRatio, tolerance = toleranceFactor2 * pxRatio, mousePos = interactivityData.mouse.position, radius = container.retina.destroyModeDistance;
  if (!radius || radius < minRadius || !mousePos) {
    return;
  }
  processDestroy(container, new Circle(mousePos.x, mousePos.y, radius + tolerance));
}

// node_modules/@tsparticles/interaction-external-destroy/browser/Options/Classes/Destroy.js
var Destroy = class {
  distance = 200;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
  }
};

// node_modules/@tsparticles/interaction-external-destroy/browser/Destroyer.js
var destroyMode = "destroy";
var Destroyer = class extends ExternalInteractorBase {
  #maxDistance;
  constructor(container) {
    super(container);
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    const container = this.container, destroy2 = container.actualOptions.interactivity?.modes.destroy;
    if (!destroy2) {
      return;
    }
    this.#maxDistance = destroy2.distance;
    container.retina.destroyModeDistance = destroy2.distance * container.retina.pixelRatio;
  }
  interact(interactivityData) {
    const container = this.container, options = container.actualOptions, events = options.interactivity?.events, mouseMoveStatus = interactivityData.status === mouseMoveEvent;
    if (!events) {
      return;
    }
    const hoverEnabled = events.onHover.enable, hoverMode = events.onHover.mode, divs = events.onDiv;
    if (mouseMoveStatus && hoverEnabled && isInArray(destroyMode, hoverMode)) {
      mouseDestroy(this.container, interactivityData);
    } else {
      divDestroy(this.container, divs, destroyMode);
    }
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    if (!events) {
      return false;
    }
    const divs = events.onDiv;
    return !!mouse.position && events.onHover.enable && isInArray(destroyMode, events.onHover.mode) || isDivModeEnabled(destroyMode, divs);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "destroy", Destroy, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-destroy/browser/index.js
async function loadExternalDestroyInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalDestroy", async (container) => {
      return Promise.resolve(new Destroyer(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-grab/browser/Options/Classes/GrabLinks.js
var GrabLinks = class {
  blink = false;
  color;
  consent = false;
  opacity = 1;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "blink", data.blink);
    if (data.color !== void 0) {
      this.color = OptionsColor.create(this.color, data.color);
    }
    loadProperty(this, "consent", data.consent);
    loadRangeProperty(this, "opacity", data.opacity);
  }
};

// node_modules/@tsparticles/interaction-external-grab/browser/Options/Classes/Grab.js
var Grab = class {
  distance = 100;
  links = new GrabLinks();
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
    this.links.load(data.links);
  }
};

// node_modules/@tsparticles/interaction-external-grab/browser/Utils.js
var defaultWidth = 0;
function drawGrabLine(context, width, begin, end, colorLine, opacity, hdr = false) {
  drawLine(context, begin, end);
  context.strokeStyle = getStyleFromRgb(colorLine, hdr, opacity);
  context.lineWidth = width;
  context.stroke();
}
function drawGrab(container, particle, lineColor, opacity, mousePos) {
  container.canvas.render.draw((ctx) => {
    const beginPos = particle.getPosition();
    drawGrabLine(ctx, particle.retina.linksWidth ?? defaultWidth, beginPos, mousePos, lineColor, opacity, container.hdr);
  });
}

// node_modules/@tsparticles/interaction-external-grab/browser/Grabber.js
var grabMode = "grab";
var minDistance4 = 0;
var minOpacity = 0;
var Grabber = class extends ExternalInteractorBase {
  #maxDistance;
  #pluginManager;
  constructor(pluginManager, container) {
    super(container);
    this.#pluginManager = pluginManager;
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    const container = this.container, grab = container.actualOptions.interactivity?.modes.grab;
    if (!grab) {
      return;
    }
    this.#maxDistance = grab.distance;
    container.retina.grabModeDistance = grab.distance * container.retina.pixelRatio;
  }
  interact(interactivityData) {
    const container = this.container, options = container.actualOptions, interactivity = options.interactivity;
    if (!interactivity?.modes.grab || !interactivity.events.onHover.enable || interactivityData.status !== mouseMoveEvent) {
      return;
    }
    const mousePos = interactivityData.mouse.position;
    if (!mousePos) {
      return;
    }
    const distance = container.retina.grabModeDistance;
    if (!distance || distance < minDistance4) {
      return;
    }
    const query = container.particles.grid.queryCircle(mousePos, distance, (p) => this.isEnabled(interactivityData, p));
    for (const particle of query) {
      const pos = particle.getPosition(), pointDistance = getDistance(pos, mousePos);
      if (pointDistance > distance) {
        continue;
      }
      const grabLineOptions = interactivity.modes.grab.links, lineOpacity = grabLineOptions.opacity, opacityLine = lineOpacity - pointDistance * lineOpacity / distance;
      if (opacityLine <= minOpacity) {
        continue;
      }
      const optColor = grabLineOptions.color ?? particle.options.links?.color;
      if (!container.particles.grabLineColor && optColor) {
        const linksOptions = interactivity.modes.grab.links;
        container.particles.grabLineColor = getLinkRandomColor(this.#pluginManager, optColor, linksOptions.blink, linksOptions.consent);
      }
      const colorLine = getLinkColor(particle, void 0, container.particles.grabLineColor);
      if (!colorLine) {
        continue;
      }
      drawGrab(container, particle, colorLine, opacityLine, mousePos);
    }
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, mouse = interactivityData.mouse, events = (particle?.interactivity ?? container.actualOptions.interactivity)?.events;
    return !!events?.onHover.enable && !!mouse.position && isInArray(grabMode, events.onHover.mode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "grab", Grab, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-grab/browser/index.js
async function loadExternalGrabInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalGrab", (container) => {
      return Promise.resolve(new Grabber(e.pluginManager, container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-parallax/browser/Options/Classes/Parallax.js
var Parallax = class {
  force = 2;
  smooth = 10;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "force", data.force);
    loadProperty(this, "smooth", data.smooth);
  }
};

// node_modules/@tsparticles/interaction-external-parallax/browser/Parallaxer.js
var parallaxMode = "parallax";
var Parallaxer = class extends ExternalInteractorBase {
  maxDistance = 0;
  constructor(container) {
    super(container);
  }
  clear() {
  }
  init() {
  }
  interact(interactivityData) {
    for (const particle of this.container.particles.filter((p) => this.isEnabled(interactivityData, p))) {
      this.#parallaxInteract(interactivityData, particle);
    }
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, mouse = interactivityData.mouse, events = (particle?.interactivity ?? container.actualOptions.interactivity)?.events;
    return !!events?.onHover.enable && !!mouse.position && isInArray(parallaxMode, events.onHover.mode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "parallax", Parallax, ...sources);
  }
  reset() {
  }
  #parallaxInteract(interactivityData, particle) {
    if (!this.isEnabled(interactivityData, particle)) {
      return;
    }
    const container = this.container, options = container.actualOptions, parallaxOptions = options.interactivity?.modes.parallax;
    if (!parallaxOptions) {
      return;
    }
    const parallaxForce = parallaxOptions.force, mousePos = interactivityData.mouse.position;
    if (!mousePos) {
      return;
    }
    const canvasSize = container.canvas.size, canvasCenter = {
      x: canvasSize.width * half,
      y: canvasSize.height * half
    }, parallaxSmooth = parallaxOptions.smooth, factor = particle.getRadius() / parallaxForce, centerDistance = {
      x: (mousePos.x - canvasCenter.x) * factor,
      y: (mousePos.y - canvasCenter.y) * factor
    }, { offset } = particle;
    offset.x += (centerDistance.x - offset.x) / parallaxSmooth;
    offset.y += (centerDistance.y - offset.y) / parallaxSmooth;
  }
};

// node_modules/@tsparticles/interaction-external-parallax/browser/index.js
async function loadExternalParallaxInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalParallax", (container) => {
      return Promise.resolve(new Parallaxer(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-pause/browser/Pauser.js
var pauseMode = "pause";
var Pauser = class extends ExternalInteractorBase {
  handleClickMode;
  maxDistance = 0;
  constructor(container) {
    super(container);
    this.handleClickMode = (mode) => {
      if (mode !== pauseMode) {
        return;
      }
      const container2 = this.container;
      if (container2.animationStatus) {
        container2.pause();
      } else {
        container2.play();
      }
    };
  }
  clear() {
  }
  init() {
  }
  interact() {
  }
  isEnabled(_interactivityData, particle) {
    const container = this.container, options = container.actualOptions, events = (particle?.interactivity ?? options.interactivity)?.events;
    return !!events && isInArray(pauseMode, events.onClick.mode);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-pause/browser/index.js
async function loadExternalPauseInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalPause", (container) => {
      return Promise.resolve(new Pauser(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-push/browser/Options/Classes/Push.js
var Push = class {
  default = true;
  groups = [];
  particles;
  quantity = 4;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "default", data.default);
    if (data.groups !== void 0) {
      this.groups = data.groups.map((t) => t);
    }
    if (!this.groups.length) {
      this.default = true;
    }
    loadRangeProperty(this, "quantity", data.quantity);
    this.particles = executeOnSingleOrMultiple(data.particles, (particles) => {
      return deepExtend({}, particles);
    });
  }
};

// node_modules/@tsparticles/interaction-external-push/browser/Pusher.js
var pushMode = "push";
var minQuantity = 0;
var Pusher = class extends ExternalInteractorBase {
  handleClickMode;
  maxDistance = 0;
  constructor(container) {
    super(container);
    this.handleClickMode = (mode, interactivityData) => {
      if (mode !== pushMode) {
        return;
      }
      const container2 = this.container, options = container2.actualOptions, pushOptions = options.interactivity?.modes.push;
      if (!pushOptions) {
        return;
      }
      const quantity = getRangeValue(pushOptions.quantity);
      if (quantity <= minQuantity) {
        return;
      }
      const group = itemFromArray([void 0, ...pushOptions.groups]), groupOptions = group !== void 0 ? container2.actualOptions.particles.groups[group] : void 0, particlesOptions = itemFromSingleOrMultiple(pushOptions.particles), overrideOptions = deepExtend(groupOptions, particlesOptions);
      container2.particles.push(quantity, interactivityData.mouse.position, overrideOptions, group);
    };
  }
  clear() {
  }
  init() {
  }
  interact() {
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    return !!events && mouse.clicking && mouse.inside && !!mouse.position && isInArray(pushMode, events.onClick.mode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "push", Push, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-push/browser/index.js
async function loadExternalPushInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalPush", (container) => {
      return Promise.resolve(new Pusher(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-remove/browser/Options/Classes/Remove.js
var Remove = class {
  quantity = 2;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadRangeProperty(this, "quantity", data.quantity);
  }
};

// node_modules/@tsparticles/interaction-external-remove/browser/Remover.js
var removeMode = "remove";
var Remover = class extends ExternalInteractorBase {
  handleClickMode;
  maxDistance = 0;
  constructor(container) {
    super(container);
    this.handleClickMode = (mode) => {
      const container2 = this.container, options = container2.actualOptions;
      if (!options.interactivity?.modes.remove || mode !== removeMode) {
        return;
      }
      const removeNb = getRangeValue(options.interactivity.modes.remove.quantity);
      for (let i = 0; i < removeNb; i++) {
        container2.particles.get(i)?.destroy();
      }
    };
  }
  clear() {
  }
  init() {
  }
  interact() {
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    return !!events && mouse.clicking && mouse.inside && !!mouse.position && isInArray(removeMode, events.onClick.mode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "remove", Remove, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-external-remove/browser/index.js
async function loadExternalRemoveInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalRemove", (container) => {
      return Promise.resolve(new Remover(container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-repulse/browser/Options/Classes/RepulseBase.js
var RepulseBase = class {
  distance = 200;
  duration = 0.4;
  easing = "ease-out-quad";
  factor = 100;
  maxSpeed = 50;
  restore;
  speed = 1;
  constructor() {
    this.restore = {
      enable: false,
      delay: 0,
      speed: 0.08,
      follow: true
    };
  }
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "distance", data.distance);
    loadProperty(this, "duration", data.duration);
    loadProperty(this, "easing", data.easing);
    loadProperty(this, "factor", data.factor);
    loadProperty(this, "speed", data.speed);
    loadProperty(this, "maxSpeed", data.maxSpeed);
    if (data.restore !== void 0) {
      this.restore.enable = data.restore.enable ?? this.restore.enable;
      this.restore.delay = data.restore.delay ?? this.restore.delay;
      this.restore.speed = data.restore.speed ?? this.restore.speed;
      this.restore.follow = data.restore.follow ?? this.restore.follow;
    }
  }
};

// node_modules/@tsparticles/interaction-external-repulse/browser/Options/Classes/RepulseDiv.js
var RepulseDiv = class extends RepulseBase {
  selectors = [];
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "selectors", data.selectors);
  }
};

// node_modules/@tsparticles/interaction-external-repulse/browser/Options/Classes/Repulse.js
var Repulse = class extends RepulseBase {
  divs;
  load(data) {
    super.load(data);
    if (isNull(data)) {
      return;
    }
    this.divs = executeOnSingleOrMultiple(data.divs, (div) => {
      const tmp = new RepulseDiv();
      tmp.load(div);
      return tmp;
    });
  }
};

// node_modules/@tsparticles/interaction-external-repulse/browser/Repulser.js
var repulseMode = "repulse";
var minDistance5 = 0;
var repulseRadiusFactor = 6;
var repulseRadiusPower = 3;
var squarePower = 2;
var minRadius3 = 0;
var minSpeed = 0;
var easingOffset = 1;
var minRestoreSpeed2 = 1e-3;
var maxRestoreSpeed2 = 1;
var restoreEpsilon2 = 0.5;
var Repulser = class extends ExternalInteractorBase {
  handleClickMode;
  #clickVec;
  #interactedThisFrame;
  #maxDistance;
  #normVec;
  #pluginManager;
  #restoreData;
  constructor(pluginManager, container) {
    super(container);
    this.#pluginManager = pluginManager;
    this.#maxDistance = 0;
    this.#normVec = Vector.origin;
    this.#interactedThisFrame = /* @__PURE__ */ new Set();
    this.#clickVec = Vector.origin;
    this.#restoreData = /* @__PURE__ */ new Map();
    container.repulse ??= { particles: [] };
    this.handleClickMode = (mode, interactivityData) => {
      const options = this.container.actualOptions, repulseOpts = options.interactivity?.modes.repulse;
      if (!repulseOpts || mode !== repulseMode) {
        return;
      }
      container.repulse ??= { particles: [] };
      const repulse = container.repulse;
      repulse.clicking = true;
      repulse.count = 0;
      for (const particle of container.repulse.particles) {
        if (!this.isEnabled(interactivityData, particle)) {
          continue;
        }
        particle.velocity.setTo(particle.initialVelocity);
      }
      repulse.particles = [];
      repulse.finish = false;
      setTimeout(() => {
        if (container.destroyed) {
          return;
        }
        repulse.clicking = false;
      }, repulseOpts.duration * millisecondsToSeconds);
    };
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    const container = this.container, repulse = container.actualOptions.interactivity?.modes.repulse;
    if (!repulse) {
      return;
    }
    this.#maxDistance = repulse.distance;
    container.retina.repulseModeDistance = repulse.distance * container.retina.pixelRatio;
  }
  interact(interactivityData) {
    this.#interactedThisFrame.clear();
    const container = this.container, options = container.actualOptions, mouseMoveStatus = interactivityData.status === mouseMoveEvent, events = options.interactivity?.events;
    if (!events) {
      return;
    }
    const hover = events.onHover, hoverEnabled = hover.enable, hoverMode = hover.mode, click = events.onClick, clickEnabled = click.enable, clickMode = click.mode, divs = events.onDiv;
    if (mouseMoveStatus && hoverEnabled && isInArray(repulseMode, hoverMode)) {
      this.#hoverRepulse(interactivityData);
    } else if (clickEnabled && isInArray(repulseMode, clickMode)) {
      this.#clickRepulse(interactivityData);
    } else {
      divModeExecute(repulseMode, divs, (selector, div) => {
        this.#singleSelectorRepulse(interactivityData, selector, div);
      });
    }
    this.#restoreParticles();
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, options = container.actualOptions, mouse = interactivityData.mouse, events = (particle?.interactivity ?? options.interactivity)?.events;
    if (!events) {
      return false;
    }
    const divs = events.onDiv, hover = events.onHover, click = events.onClick, divRepulse = isDivModeEnabled(repulseMode, divs);
    if (!(divRepulse || hover.enable && !!mouse.position || click.enable && mouse.clickPosition)) {
      return false;
    }
    const hoverMode = hover.mode, clickMode = click.mode;
    return isInArray(repulseMode, hoverMode) || isInArray(repulseMode, clickMode) || divRepulse;
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "repulse", Repulse, ...sources);
  }
  reset() {
  }
  #clickRepulse(interactivityData) {
    const container = this.container, repulseOptions = container.actualOptions.interactivity?.modes.repulse;
    if (!repulseOptions) {
      return;
    }
    const repulse = container.repulse ?? { particles: [] };
    if (!repulse.finish) {
      repulse.count ??= 0;
      repulse.count++;
      if (repulse.count === container.particles.count) {
        repulse.finish = true;
      }
    }
    if (repulse.clicking) {
      const repulseDistance = container.retina.repulseModeDistance;
      if (!repulseDistance || repulseDistance < minDistance5) {
        return;
      }
      const repulseRadius = Math.pow(repulseDistance / repulseRadiusFactor, repulseRadiusPower), mouseClickPos = interactivityData.mouse.clickPosition;
      if (mouseClickPos === void 0) {
        return;
      }
      const range = new Circle(mouseClickPos.x, mouseClickPos.y, repulseRadius), query = container.particles.grid.query(range, (p) => this.isEnabled(interactivityData, p));
      for (const particle of query) {
        const { dx, dy, distance } = getDistances(mouseClickPos, particle.position), d = distance ** squarePower, velocity = repulseOptions.speed, force = -repulseRadius * velocity / d;
        if (d <= repulseRadius) {
          this.#trackInteractedParticle(particle);
          repulse.particles.push(particle);
          this.#clickVec.x = dx;
          this.#clickVec.y = dy;
          this.#clickVec.length = force;
          particle.velocity.setTo(this.#clickVec);
        }
      }
    } else if (repulse.clicking === false) {
      for (const particle of repulse.particles) {
        particle.velocity.setTo(particle.initialVelocity);
      }
      repulse.particles = [];
    }
  }
  #hoverRepulse(interactivityData) {
    const container = this.container, mousePos = interactivityData.mouse.position, repulseRadius = container.retina.repulseModeDistance;
    if (!repulseRadius || repulseRadius < minRadius3 || !mousePos) {
      return;
    }
    this.#processRepulse(interactivityData, mousePos, repulseRadius, new Circle(mousePos.x, mousePos.y, repulseRadius));
  }
  #processRepulse(interactivityData, position, repulseRadius, area, divRepulse) {
    const container = this.container, query = container.particles.grid.query(area, (p) => this.isEnabled(interactivityData, p)), repulseOptions = container.actualOptions.interactivity?.modes.repulse;
    if (!repulseOptions) {
      return;
    }
    const { easing, speed, factor, maxSpeed } = repulseOptions, easingFunc = this.#pluginManager.getEasing(easing), velocity = (divRepulse?.speed ?? speed) * factor;
    for (const particle of query) {
      const { dx, dy, distance } = getDistances(particle.position, position), repulseFactor = clamp(easingFunc(easingOffset - distance / repulseRadius) * velocity, minSpeed, maxSpeed);
      this.#normVec.x = !distance ? velocity : dx / distance * repulseFactor;
      this.#normVec.y = !distance ? velocity : dy / distance * repulseFactor;
      this.#trackInteractedParticle(particle);
      particle.position.addTo(this.#normVec);
    }
  }
  #restoreParticles() {
    const restore = this.container.actualOptions.interactivity?.modes.repulse?.restore;
    if (!restore?.enable || !this.#restoreData.size) {
      return;
    }
    const now = Date.now(), restoreDelay = restore.delay * millisecondsToSeconds, restoreSpeed = Math.max(minRestoreSpeed2, Math.min(maxRestoreSpeed2, restore.speed));
    for (const [particle, restoreData] of this.#restoreData) {
      if (this.#interactedThisFrame.has(particle)) {
        continue;
      }
      if (particle.destroyed) {
        this.#restoreData.delete(particle);
        continue;
      }
      const target = restoreData.target;
      if (now - restoreData.lastInteractionTime < restoreDelay) {
        continue;
      }
      if (restore.follow && particle.options.move.enable) {
        target.x += particle.velocity.x;
        target.y += particle.velocity.y;
        target.z += particle.velocity.z;
      }
      const dx = target.x - particle.position.x, dy = target.y - particle.position.y, dz = target.z - particle.position.z;
      particle.position.x += dx * restoreSpeed;
      particle.position.y += dy * restoreSpeed;
      particle.position.z += dz * restoreSpeed;
      if (Math.abs(dx) <= restoreEpsilon2 && Math.abs(dy) <= restoreEpsilon2) {
        particle.position.x = target.x;
        particle.position.y = target.y;
        particle.position.z = target.z;
        this.#restoreData.delete(particle);
        continue;
      }
    }
  }
  #singleSelectorRepulse(interactivityData, selector, div) {
    const container = this.container, repulse = container.actualOptions.interactivity?.modes.repulse;
    if (!repulse) {
      return;
    }
    const query = safeDocument().querySelectorAll(selector);
    if (!query.length) {
      return;
    }
    query.forEach((item) => {
      const elem = item, pxRatio = container.retina.pixelRatio, pos = {
        x: (elem.offsetLeft + elem.offsetWidth * half) * pxRatio,
        y: (elem.offsetTop + elem.offsetHeight * half) * pxRatio
      }, repulseRadius = elem.offsetWidth * half * pxRatio, area = div.type === DivType.circle ? new Circle(pos.x, pos.y, repulseRadius) : new Rectangle(elem.offsetLeft * pxRatio, elem.offsetTop * pxRatio, elem.offsetWidth * pxRatio, elem.offsetHeight * pxRatio), divs = repulse.divs, divRepulse = divMode(divs, elem);
      this.#processRepulse(interactivityData, pos, repulseRadius, area, divRepulse);
    });
  }
  #trackInteractedParticle(particle) {
    this.#interactedThisFrame.add(particle);
    const restore = this.container.actualOptions.interactivity?.modes.repulse?.restore;
    if (!restore?.enable) {
      return;
    }
    const now = Date.now();
    let restoreData = this.#restoreData.get(particle);
    if (!restoreData) {
      restoreData = {
        target: particle.position.copy(),
        lastInteractionTime: now
      };
      this.#restoreData.set(particle, restoreData);
    }
    restoreData.lastInteractionTime = now;
    if (restore.follow && particle.options.move.enable) {
      restoreData.target.x += particle.velocity.x;
      restoreData.target.y += particle.velocity.y;
      restoreData.target.z += particle.velocity.z;
    }
  }
};

// node_modules/@tsparticles/interaction-external-repulse/browser/index.js
async function loadExternalRepulseInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    const pluginManager = e.pluginManager;
    pluginManager.addInteractor?.("externalRepulse", (container) => {
      return Promise.resolve(new Repulser(pluginManager, container));
    });
  });
}

// node_modules/@tsparticles/interaction-external-slow/browser/Options/Classes/Slow.js
var Slow = class {
  factor = 3;
  radius = 200;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "factor", data.factor);
    loadProperty(this, "radius", data.radius);
  }
};

// node_modules/@tsparticles/interaction-external-slow/browser/SlowModifier.js
var SlowModifier = class {
  enabled = false;
  id = "slow";
  priority = 100;
  speedFactor = 1;
};

// node_modules/@tsparticles/interaction-external-slow/browser/Slower.js
var slowMode = "slow";
var minRadius4 = 0;
var Slower = class extends ExternalInteractorBase {
  #maxDistance;
  #modifiers = /* @__PURE__ */ new WeakMap();
  constructor(container) {
    super(container);
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear(particle, _delta, force) {
    const mod = this.#modifiers.get(particle);
    if (mod?.enabled && !force) {
      return;
    }
    particle.removeModifier(slowMode);
    this.#modifiers.delete(particle);
  }
  getOrCreateModifier(particle) {
    let mod = this.#modifiers.get(particle);
    if (!mod) {
      mod = new SlowModifier();
      this.#modifiers.set(particle, mod);
      particle.addModifier(mod);
    }
    return mod;
  }
  init() {
    const container = this.container, slow = container.actualOptions.interactivity?.modes.slow;
    if (!slow) {
      return;
    }
    this.#maxDistance = slow.radius;
    container.retina.slowModeRadius = slow.radius * container.retina.pixelRatio;
  }
  interact() {
  }
  isEnabled(interactivityData, particle) {
    const container = this.container, mouse = interactivityData.mouse, events = (particle?.interactivity ?? container.actualOptions.interactivity)?.events;
    return !!events?.onHover.enable && !!mouse.position && isInArray(slowMode, events.onHover.mode);
  }
  loadModeOptions(options, ...sources) {
    loadOptionProperty(options, "slow", Slow, ...sources);
  }
  reset(interactivityData, particle) {
    const mod = this.#modifiers.get(particle);
    if (mod) {
      mod.enabled = false;
    }
    const container = this.container, options = container.actualOptions, mousePos = interactivityData.mouse.position, radius = container.retina.slowModeRadius, slowOptions = options.interactivity?.modes.slow;
    if (!slowOptions || !radius || radius < minRadius4 || !mousePos) {
      return;
    }
    const particlePos = particle.getPosition(), dist = getDistance(mousePos, particlePos), proximityFactor = dist / radius, slowFactor = slowOptions.factor;
    if (dist > radius) {
      return;
    }
    const activeMod = this.getOrCreateModifier(particle);
    activeMod.enabled = true;
    activeMod.speedFactor = proximityFactor / slowFactor;
  }
};

// node_modules/@tsparticles/interaction-external-slow/browser/index.js
async function loadExternalSlowInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("externalSlow", (container) => {
      return Promise.resolve(new Slower(container));
    });
  });
}

// node_modules/@tsparticles/shape-image/browser/Utils.js
var shapeTypes = ["image", "images"];
var stringStart = 0;
var defaultOpacity3 = 1;
var currentColorRegex = /(#(?:[0-9a-f]{2}){2,4}|(#[0-9a-f]{3})|(rgb|hsl)a?\((-?\d+%?[,\s]+){2,3}\s*[\d.]+%?\))|currentcolor/gi;
function replaceColorSvg(imageShape, color, opacity, hdr = false) {
  const { svgData } = imageShape;
  if (!svgData) {
    return "";
  }
  const colorStyle = getStyleFromHsl(color, hdr, opacity);
  if (svgData.includes("fill")) {
    return svgData.replaceAll(currentColorRegex, () => colorStyle);
  }
  const preFillIndex = svgData.indexOf(">");
  return `${svgData.substring(stringStart, preFillIndex)} fill="${colorStyle}"${svgData.substring(preFillIndex)}`;
}
async function loadImage(image) {
  return new Promise((resolve) => {
    image.loading = true;
    const img = new Image();
    image.element = img;
    img.addEventListener("load", () => {
      image.loading = false;
      resolve();
    });
    img.addEventListener("error", () => {
      image.element = void 0;
      image.error = true;
      image.loading = false;
      getLogger().error(`Error loading image: ${image.source}`);
      resolve();
    });
    img.src = image.source;
  });
}
async function downloadSvgImage(image) {
  if (image.type !== "svg") {
    await loadImage(image);
    return;
  }
  image.loading = true;
  const response = await fetch(image.source);
  if (response.ok) {
    image.svgData = await response.text();
  } else {
    getLogger().error("Image not found");
    image.error = true;
  }
  image.loading = false;
}
function replaceImageColor(image, imageData, color, particle, hdr = false) {
  const svgColoredData = replaceColorSvg(image, color, particle.opacity?.value ?? defaultOpacity3, hdr), imageRes = {
    color,
    data: __spreadProps(__spreadValues({}, image), {
      svgData: svgColoredData
    }),
    loaded: false,
    ratio: imageData.width / imageData.height,
    replaceColor: imageData.replaceColor,
    source: imageData.src
  };
  return new Promise((resolve) => {
    const svg = new Blob([svgColoredData], { type: "image/svg+xml" }), url = URL.createObjectURL(svg), img = new Image();
    img.addEventListener("load", () => {
      imageRes.loaded = true;
      imageRes.element = img;
      resolve(imageRes);
      URL.revokeObjectURL(url);
    });
    const errorHandler = async () => {
      URL.revokeObjectURL(url);
      const img2 = __spreadProps(__spreadValues({}, image), {
        error: false,
        loading: true
      });
      await loadImage(img2);
      imageRes.loaded = true;
      imageRes.element = img2.element;
      resolve(imageRes);
    };
    img.addEventListener("error", () => void errorHandler());
    img.src = url;
  });
}

// node_modules/@tsparticles/shape-image/browser/ImageDrawer.js
var sides2 = 12;
var ImageDrawer = class {
  #container;
  #engine;
  constructor(engine, container) {
    this.#engine = engine;
    this.#container = container;
  }
  draw(data) {
    const { context, radius, particle, opacity } = data, image = particle.image, element = image?.element;
    if (!image) {
      return;
    }
    context.globalAlpha = opacity;
    if (element) {
      const ratio = image.ratio, pos = {
        x: -radius,
        y: -radius
      }, diameter = radius * double;
      context.drawImage(element, pos.x, pos.y, diameter, diameter / ratio);
    }
    context.globalAlpha = defaultAlpha;
  }
  getSidesCount() {
    return sides2;
  }
  async init(container) {
    const options = container.actualOptions;
    if (!options.preload || !this.#engine.loadImage) {
      return;
    }
    const promises = [];
    for (const imageData of options.preload) {
      promises.push(this.#engine.loadImage(container, imageData));
    }
    await Promise.all(promises);
  }
  loadShape(particle) {
    const container = this.#container;
    if (!particle.shape || !shapeTypes.includes(particle.shape)) {
      return;
    }
    const imageData = particle.shapeData;
    if (!imageData) {
      return;
    }
    const images = this.#engine.getImages?.(container), image = images?.find((t) => t.name === imageData.name || t.source === imageData.src);
    if (image) {
      return;
    }
    void this.#loadImageShape(container, imageData).then(() => {
      this.loadShape(particle);
    });
  }
  particleInit(container, particle) {
    if (particle.shape !== "image" && particle.shape !== "images") {
      return;
    }
    const images = this.#engine.getImages?.(container), imageData = particle.shapeData;
    if (!imageData) {
      return;
    }
    const color = particle.getFillColor(), image = images?.find((t) => t.name === imageData.name || t.source === imageData.src);
    if (!image) {
      return;
    }
    const replaceColor = imageData.replaceColor;
    if (image.loading) {
      setTimeout(() => {
        this.particleInit(container, particle);
      });
      return;
    }
    void (async () => {
      let imageRes;
      if (image.svgData && color) {
        imageRes = await replaceImageColor(image, imageData, color, particle, container.hdr);
      } else {
        imageRes = {
          color,
          data: image,
          element: image.element,
          loaded: true,
          ratio: imageData.width && imageData.height ? imageData.width / imageData.height : image.ratio ?? defaultRatio,
          replaceColor,
          source: imageData.src
        };
      }
      if (!imageRes.ratio) {
        imageRes.ratio = 1;
      }
      const close = imageData.close ?? particle.shapeClose, imageShape = {
        image: imageRes,
        close
      };
      particle.image = imageShape.image;
      particle.shapeClose = imageShape.close;
    })();
  }
  #loadImageShape = async (container, imageShape) => {
    if (!this.#engine.loadImage) {
      throw new Error(`Image shape not initialized`);
    }
    await this.#engine.loadImage(container, {
      name: imageShape.name,
      replaceColor: imageShape.replaceColor,
      src: imageShape.src
    });
  };
};

// node_modules/@tsparticles/shape-image/browser/Options/Classes/Preload.js
var Preload = class {
  height;
  name;
  replaceColor;
  src = "";
  width;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "height", data.height);
    loadProperty(this, "name", data.name);
    loadProperty(this, "replaceColor", data.replaceColor);
    loadProperty(this, "src", data.src);
    loadProperty(this, "width", data.width);
  }
};

// node_modules/@tsparticles/shape-image/browser/ImagePreloader.js
var ImagePreloaderPlugin = class {
  id = "image-preloader";
  #engine;
  constructor(engine) {
    this.#engine = engine;
  }
  async getPlugin(container) {
    const { ImagePreloaderInstance } = await import("./ImagePreloaderInstance-MGVY5T3W.js");
    return new ImagePreloaderInstance(this.#engine, container);
  }
  loadOptions(_container, options, source) {
    if (!source?.preload) {
      return;
    }
    options.preload ??= [];
    const preloadOptions = options.preload;
    for (const item of source.preload) {
      const existing = preloadOptions.find((t) => t.name === item.name || t.src === item.src);
      if (existing) {
        existing.load(item);
      } else {
        const preload = new Preload();
        preload.load(item);
        preloadOptions.push(preload);
      }
    }
  }
  needsPlugin() {
    return true;
  }
};

// node_modules/@tsparticles/shape-image/browser/index.js
var extLength = 3;
function addLoadImageToEngine(engine) {
  engine.getImages ??= (container) => {
    engine.images ??= /* @__PURE__ */ new Map();
    let images = engine.images.get(container);
    if (!images) {
      images = [];
      engine.images.set(container, images);
    }
    return images;
  };
  engine.loadImage ??= async (container, data) => {
    if (!engine.getImages) {
      throw new Error("No images collection found");
    }
    if (!data.name && !data.src) {
      throw new Error("No image source provided");
    }
    engine.images ??= /* @__PURE__ */ new Map();
    const containerImages = engine.getImages(container);
    if (containerImages.some((t) => t.name === data.name || t.source === data.src)) {
      return;
    }
    try {
      const image = {
        name: data.name ?? data.src,
        source: data.src,
        type: data.src.substring(data.src.length - extLength),
        error: false,
        loading: true,
        replaceColor: data.replaceColor,
        ratio: data.width && data.height ? data.width / data.height : void 0
      };
      containerImages.push(image);
      engine.images.set(container, containerImages);
      let imageFunc;
      if (data.replaceColor) {
        imageFunc = downloadSvgImage;
      } else {
        imageFunc = loadImage;
      }
      await imageFunc(image);
    } catch {
      throw new Error(`${data.name ?? data.src} not found`);
    }
  };
}
async function loadImageShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    addLoadImageToEngine(e);
    e.pluginManager.addPlugin(new ImagePreloaderPlugin(e));
    e.pluginManager.addShape(shapeTypes, (container) => Promise.resolve(new ImageDrawer(e, container)));
  });
}

// node_modules/@tsparticles/updater-life/browser/Options/Classes/LifeDelay.js
var LifeDelay = class extends ValueWithRandom {
  sync = false;
  load(data) {
    if (isNull(data)) {
      return;
    }
    super.load(data);
    loadProperty(this, "sync", data.sync);
  }
};

// node_modules/@tsparticles/updater-life/browser/Options/Classes/LifeDuration.js
var LifeDuration = class extends ValueWithRandom {
  sync = false;
  load(data) {
    if (isNull(data)) {
      return;
    }
    super.load(data);
    loadProperty(this, "sync", data.sync);
  }
};

// node_modules/@tsparticles/updater-life/browser/Options/Classes/Life.js
var Life = class {
  count = 0;
  delay = new LifeDelay();
  duration = new LifeDuration();
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "count", data.count);
    this.delay.load(data.delay);
    this.duration.load(data.duration);
  }
};

// node_modules/@tsparticles/updater-life/browser/Utils.js
var noTime = 0;
var infiniteValue = -1;
var noLife = 0;
var minCanvasSize = 0;
function updateLife(particle, delta, canvasSize) {
  if (!particle.life) {
    return;
  }
  const life = particle.life;
  let justSpawned = false;
  if (particle.spawning) {
    life.delayTime += delta.value;
    if (life.delayTime >= particle.life.delay) {
      justSpawned = true;
      particle.spawning = false;
      life.delayTime = noTime;
      life.time = noTime;
    } else {
      return;
    }
  }
  if (life.duration === infiniteValue) {
    return;
  }
  if (justSpawned) {
    life.time = noTime;
  } else {
    life.time += delta.value;
  }
  if (life.time < life.duration) {
    return;
  }
  life.time = noTime;
  if (particle.life.count > noLife) {
    particle.life.count--;
  }
  if (particle.life.count === noLife) {
    particle.destroy();
    return;
  }
  const widthRange = setRangeValue(minCanvasSize, canvasSize.width), heightRange = setRangeValue(minCanvasSize, canvasSize.width);
  particle.position.x = randomInRangeValue(widthRange);
  particle.position.y = randomInRangeValue(heightRange);
  particle.spawning = true;
  life.delayTime = noTime;
  life.time = noTime;
  particle.reset();
  const lifeOptions = particle.options.life;
  if (lifeOptions) {
    life.delay = getRangeValue(lifeOptions.delay.value) * millisecondsToSeconds;
    life.duration = getRangeValue(lifeOptions.duration.value) * millisecondsToSeconds;
  }
}

// node_modules/@tsparticles/updater-life/browser/LifeUpdater.js
var noTime2 = 0;
var identity2 = 1;
var infiniteValue2 = -1;
var LifeUpdater = class {
  #container;
  constructor(container) {
    this.#container = container;
  }
  init(particle) {
    const container = this.#container, particlesOptions = particle.options, lifeOptions = particlesOptions.life;
    if (!lifeOptions) {
      return;
    }
    const delayFactor = lifeOptions.delay.sync ? identity2 : getRandom(), durationFactor = lifeOptions.duration.sync ? identity2 : getRandom();
    particle.life = {
      delay: container.retina.reduceFactor ? getRangeValue(lifeOptions.delay.value) * delayFactor / container.retina.reduceFactor * millisecondsToSeconds : noTime2,
      delayTime: noTime2,
      duration: container.retina.reduceFactor ? getRangeValue(lifeOptions.duration.value) * durationFactor / container.retina.reduceFactor * millisecondsToSeconds : noTime2,
      time: noTime2,
      count: lifeOptions.count
    };
    if (particle.life.duration <= noTime2) {
      particle.life.duration = infiniteValue2;
    }
    if (particle.life.count <= noTime2) {
      particle.life.count = infiniteValue2;
    }
    particle.spawning = particle.life.delay > noTime2;
  }
  isEnabled(particle) {
    return !particle.destroyed;
  }
  loadOptions(options, ...sources) {
    loadOptionProperty(options, "life", Life, ...sources);
  }
  update(particle, delta) {
    if (!this.isEnabled(particle) || !particle.life) {
      return;
    }
    updateLife(particle, delta, this.#container.canvas.size);
  }
};

// node_modules/@tsparticles/updater-life/browser/index.js
async function loadLifeUpdater(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addParticleUpdater("life", (container) => {
      return Promise.resolve(new LifeUpdater(container));
    });
  });
}

// node_modules/@tsparticles/shape-line/browser/Utils.js
function drawLine2(data) {
  const { context, particle, radius } = data, shapeData = particle.shapeData, centerY = 0;
  context.moveTo(-radius, centerY);
  context.lineTo(radius, centerY);
  context.lineCap = shapeData?.cap ?? "butt";
}

// node_modules/@tsparticles/shape-line/browser/LineDrawer.js
var sides3 = 1;
var LineDrawer = class {
  draw(data) {
    drawLine2(data);
  }
  getSidesCount() {
    return sides3;
  }
};

// node_modules/@tsparticles/shape-line/browser/index.js
async function loadLineShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(["line"], () => Promise.resolve(new LineDrawer()));
  });
}

// node_modules/@tsparticles/interaction-particles-attract/browser/Options/Classes/Attract.js
var Attract2 = class {
  distance = 200;
  enable = false;
  rotate;
  constructor() {
    this.rotate = {
      x: 3e3,
      y: 3e3
    };
  }
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadRangeProperty(this, "distance", data.distance);
    loadProperty(this, "enable", data.enable);
    if (data.rotate) {
      const rotateX = data.rotate.x;
      if (rotateX !== void 0) {
        this.rotate.x = rotateX;
      }
      const rotateY = data.rotate.y;
      if (rotateY !== void 0) {
        this.rotate.y = rotateY;
      }
    }
  }
};

// node_modules/@tsparticles/interaction-particles-attract/browser/Attractor.js
var attractFactor = 1e3;
var identity3 = 1;
var Attractor2 = class extends ParticlesInteractorBase {
  #maxDistance;
  constructor(container) {
    super(container);
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
  }
  interact(p1) {
    if (!p1.options.attract?.enable) {
      return;
    }
    const container = this.container;
    if (isNull(p1.attractDistance)) {
      const attractDistance = getRangeValue(p1.options.attract.distance);
      if (attractDistance > this.#maxDistance) {
        this.#maxDistance = attractDistance;
      }
      p1.attractDistance = attractDistance * container.retina.pixelRatio;
    }
    const distance = p1.attractDistance, pos1 = p1.getPosition(), query = container.particles.grid.queryCircle(pos1, distance);
    for (const p2 of query) {
      if (p1 === p2 || !p2.options.attract?.enable || p2.destroyed || p2.spawning) {
        continue;
      }
      const pos2 = p2.getPosition(), { dx, dy } = getDistances(pos1, pos2), rotate = p1.options.attract.rotate, ax = dx / (rotate.x * attractFactor), ay = dy / (rotate.y * attractFactor), p1Factor = p2.size.value / p1.size.value, p2Factor = identity3 / p1Factor;
      p1.velocity.x -= ax * p1Factor;
      p1.velocity.y -= ay * p1Factor;
      p2.velocity.x += ax * p2Factor;
      p2.velocity.y += ay * p2Factor;
    }
  }
  isEnabled(particle) {
    return particle.options.attract?.enable ?? false;
  }
  loadParticlesOptions(options, ...sources) {
    loadOptionProperty(options, "attract", Attract2, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-particles-attract/browser/index.js
async function loadParticlesAttractInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addInteractor?.("particlesAttract", (container) => {
      return Promise.resolve(new Attractor2(container));
    });
  });
}

// node_modules/@tsparticles/interaction-particles-collisions/browser/CollisionMode.js
var CollisionMode;
(function(CollisionMode2) {
  CollisionMode2["absorb"] = "absorb";
  CollisionMode2["bounce"] = "bounce";
  CollisionMode2["destroy"] = "destroy";
})(CollisionMode || (CollisionMode = {}));

// node_modules/@tsparticles/interaction-particles-collisions/browser/Options/Classes/CollisionsAbsorb.js
var CollisionsAbsorb = class {
  speed = 2;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "speed", data.speed);
  }
};

// node_modules/@tsparticles/interaction-particles-collisions/browser/Options/Classes/CollisionsOverlap.js
var CollisionsOverlap = class {
  enable = true;
  retries = 0;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "enable", data.enable);
    loadProperty(this, "retries", data.retries);
  }
};

// node_modules/@tsparticles/interaction-particles-collisions/browser/Options/Classes/Collisions.js
var Collisions = class {
  absorb = new CollisionsAbsorb();
  bounce = new ParticlesBounce();
  enable = false;
  maxSpeed = 50;
  mode = CollisionMode.bounce;
  overlap = new CollisionsOverlap();
  load(data) {
    if (isNull(data)) {
      return;
    }
    this.absorb.load(data.absorb);
    this.bounce.load(data.bounce);
    loadProperty(this, "enable", data.enable);
    loadRangeProperty(this, "maxSpeed", data.maxSpeed);
    loadProperty(this, "mode", data.mode);
    this.overlap.load(data.overlap);
  }
};

// node_modules/@tsparticles/interaction-particles-collisions/browser/Absorb.js
var minAbsorbAmount = 0;
function updateAbsorb(p1, r1, p2, r2, delta, pixelRatio) {
  if (!p1.options.collisions || !p2.options.collisions) {
    return;
  }
  const absorbSpeed = p1.options.collisions.absorb.speed, shrinkAmount = clamp(absorbSpeed * delta.factor, minAbsorbAmount, r2);
  p1.size.value = Math.sqrt(r1 * r1 + shrinkAmount * shrinkAmount);
  p2.size.value -= shrinkAmount;
  if (p2.size.value <= pixelRatio) {
    p2.size.value = 0;
    p2.destroy();
  }
}
function absorb(p1, p2, delta, pixelRatio) {
  const r1 = p1.getRadius(), r2 = p2.getRadius();
  if (!r1 && r2) {
    p1.destroy();
  } else if (r1 && !r2) {
    p2.destroy();
  } else if (r1 && r2) {
    if (r1 >= r2) {
      updateAbsorb(p1, r1, p2, r2, delta, pixelRatio);
    } else {
      updateAbsorb(p2, r2, p1, r1, delta, pixelRatio);
    }
  }
}

// node_modules/@tsparticles/interaction-particles-collisions/browser/Bounce.js
var energyCorrectionMinRatio = 1e-6;
var energyDriftThreshold = 1e-4;
var correctionFactorNeutral = 1;
var fixBounceSpeed = (p) => {
  if (!p.options.collisions) {
    return;
  }
  p.collisionMaxSpeed ??= getRangeValue(p.options.collisions.maxSpeed);
  if (p.velocity.length > p.collisionMaxSpeed) {
    p.velocity.length = p.collisionMaxSpeed;
  }
};
function bounce(p1, p2) {
  const m1 = p1.getMass(), m2 = p2.getMass(), speed1Before = p1.velocity.length, speed2Before = p2.velocity.length, keBefore = m1 * speed1Before * speed1Before + m2 * speed2Before * speed2Before;
  circleBounce(circleBounceDataFromParticle(p1), circleBounceDataFromParticle(p2));
  const speed1After = p1.velocity.length, speed2After = p2.velocity.length, keAfter = m1 * speed1After * speed1After + m2 * speed2After * speed2After;
  if (keAfter > keBefore * energyCorrectionMinRatio) {
    const correctionFactor = Math.sqrt(keBefore / keAfter);
    if (Math.abs(correctionFactor - correctionFactorNeutral) > energyDriftThreshold) {
      p1.velocity.length = speed1After * correctionFactor;
      p2.velocity.length = speed2After * correctionFactor;
    }
  }
  fixBounceSpeed(p1);
  fixBounceSpeed(p2);
}

// node_modules/@tsparticles/interaction-particles-collisions/browser/Destroy.js
function destroy(p1, p2) {
  if (!p1.unbreakable && !p2.unbreakable) {
    bounce(p1, p2);
  }
  const p1Radius = p1.getRadius(), p2Radius = p2.getRadius();
  if (!p1Radius && p2Radius) {
    p1.destroy();
  } else if (p1Radius && !p2Radius) {
    p2.destroy();
  } else if (p1Radius && p2Radius) {
    const deleteP = p1.getRadius() >= p2.getRadius() ? p2 : p1;
    deleteP.destroy();
  }
}

// node_modules/@tsparticles/interaction-particles-collisions/browser/ResolveCollision.js
function resolveCollision(p1, p2, delta, pixelRatio) {
  if (!p1.options.collisions || !p2.options.collisions) {
    return;
  }
  switch (p1.options.collisions.mode) {
    case CollisionMode.absorb: {
      absorb(p1, p2, delta, pixelRatio);
      break;
    }
    case CollisionMode.bounce: {
      bounce(p1, p2);
      break;
    }
    case CollisionMode.destroy: {
      destroy(p1, p2);
      break;
    }
    default:
      break;
  }
}

// node_modules/@tsparticles/interaction-particles-collisions/browser/Collider.js
var Collider = class extends ParticlesInteractorBase {
  maxDistance;
  constructor(container) {
    super(container);
    this.maxDistance = 0;
  }
  clear() {
  }
  init() {
  }
  interact(p1, _interactivityData, delta) {
    if (p1.destroyed || p1.spawning) {
      return;
    }
    const container = this.container, pos1 = p1.getPosition(), radius1 = p1.getRadius(), query = container.particles.grid.queryCircle(pos1, radius1 * double);
    for (const p2 of query) {
      if (p1 === p2 || p1.id >= p2.id || !p1.options.collisions?.enable || !p2.options.collisions?.enable || p1.options.collisions.mode !== p2.options.collisions.mode || p2.destroyed || p2.spawning) {
        continue;
      }
      const pos2 = p2.getPosition(), radius2 = p2.getRadius();
      if (Math.abs(Math.round(pos1.z) - Math.round(pos2.z)) > radius1 + radius2) {
        continue;
      }
      const dist = getDistance(pos1, pos2), distP = radius1 + radius2;
      if (dist > distP) {
        continue;
      }
      resolveCollision(p1, p2, delta, container.retina.pixelRatio);
    }
  }
  isEnabled(particle) {
    return !!particle.options.collisions?.enable;
  }
  loadParticlesOptions(options, ...sources) {
    loadOptionProperty(options, "collisions", Collisions, ...sources);
  }
  reset() {
  }
};

// node_modules/@tsparticles/interaction-particles-collisions/browser/OverlapPlugin.js
var OverlapPlugin = class {
  id = "overlap";
  async getPlugin(container) {
    const { OverlapPluginInstance } = await import("./OverlapPluginInstance-A5MZUD6N.js");
    return new OverlapPluginInstance(container);
  }
  loadOptions() {
  }
  needsPlugin() {
    return true;
  }
};

// node_modules/@tsparticles/interaction-particles-collisions/browser/index.js
async function loadParticlesCollisionsInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    ensureInteractivityPluginLoaded(e);
    e.pluginManager.addPlugin(new OverlapPlugin());
    e.pluginManager.addInteractor?.("particlesCollisions", (container) => {
      return Promise.resolve(new Collider(container));
    });
  });
}

// node_modules/@tsparticles/interaction-particles-links/browser/CircleWarp.js
var CircleWarp = class extends Circle {
  #canvasSize;
  constructor(x, y, radius, canvasSize) {
    super(x, y, radius);
    this.#canvasSize = canvasSize;
  }
  contains(point) {
    if (super.contains(point))
      return true;
    const { width, height } = this.#canvasSize, { x, y } = point;
    return super.contains({ x: x - width, y }) || super.contains({ x: x + width, y }) || super.contains({ x, y: y - height }) || super.contains({ x, y: y + height }) || super.contains({ x: x - width, y: y - height }) || super.contains({ x: x + width, y: y + height }) || super.contains({ x: x - width, y: y + height }) || super.contains({ x: x + width, y: y - height });
  }
  intersects(range) {
    if (super.intersects(range))
      return true;
    const { width, height } = this.#canvasSize, pos = range.position, shifts = [
      { x: -width, y: 0 },
      { x: width, y: 0 },
      { x: 0, y: -height },
      { x: 0, y: height },
      { x: -width, y: -height },
      { x: width, y: height },
      { x: -width, y: height },
      { x: width, y: -height }
    ];
    for (const shift of shifts) {
      const shiftedPos = { x: pos.x + shift.x, y: pos.y + shift.y };
      let shiftedRange;
      if (range instanceof Circle) {
        shiftedRange = new Circle(shiftedPos.x, shiftedPos.y, range.radius);
      } else {
        const rect = range;
        shiftedRange = new Rectangle(shiftedPos.x, shiftedPos.y, rect.size.width, rect.size.height);
      }
      if (super.intersects(shiftedRange))
        return true;
    }
    return false;
  }
};

// node_modules/@tsparticles/interaction-particles-links/browser/Options/Classes/LinksShadow.js
var LinksShadow = class {
  blur = 5;
  color = new OptionsColor();
  enable = false;
  constructor() {
    this.color.value = "#000";
  }
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "blur", data.blur);
    this.color = OptionsColor.create(this.color, data.color);
    loadProperty(this, "enable", data.enable);
  }
};

// node_modules/@tsparticles/interaction-particles-links/browser/Options/Classes/LinksTriangle.js
var LinksTriangle = class {
  color;
  enable = false;
  frequency = 1;
  opacity;
  load(data) {
    if (isNull(data)) {
      return;
    }
    if (data.color !== void 0) {
      this.color = OptionsColor.create(this.color, data.color);
    }
    loadProperty(this, "enable", data.enable);
    loadProperty(this, "frequency", data.frequency);
    loadProperty(this, "opacity", data.opacity);
  }
};

// node_modules/@tsparticles/interaction-particles-links/browser/Options/Classes/Links.js
var Links = class {
  blink = false;
  color = new OptionsColor();
  consent = false;
  distance = 100;
  enable = false;
  frequency = 1;
  id;
  opacity = 1;
  shadow = new LinksShadow();
  triangles = new LinksTriangle();
  warp = false;
  width = 1;
  constructor() {
    this.color.value = "#fff";
  }
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "id", data.id);
    loadProperty(this, "blink", data.blink);
    this.color = OptionsColor.create(this.color, data.color);
    loadProperty(this, "consent", data.consent);
    loadProperty(this, "distance", data.distance);
    loadProperty(this, "enable", data.enable);
    loadProperty(this, "frequency", data.frequency);
    loadProperty(this, "opacity", data.opacity);
    this.shadow.load(data.shadow);
    this.triangles.load(data.triangles);
    loadProperty(this, "width", data.width);
    loadProperty(this, "warp", data.warp);
  }
};

// node_modules/@tsparticles/interaction-particles-links/browser/Linker.js
var opacityOffset = 1;
var minDistance6 = 0;
function getWarpDistance(pos1, pos2, canvasSize) {
  const { dx, dy } = getDistances(pos1, pos2), absDiffs = { x: Math.abs(dx), y: Math.abs(dy) }, warpDistances = {
    x: Math.min(absDiffs.x, canvasSize.width - absDiffs.x),
    y: Math.min(absDiffs.y, canvasSize.height - absDiffs.y)
  };
  return Math.hypot(warpDistances.x, warpDistances.y);
}
var Linker = class extends ParticlesInteractorBase {
  #maxDistance;
  #pluginManager;
  constructor(pluginManager, container) {
    super(container);
    this.#pluginManager = pluginManager;
    this.#maxDistance = 0;
  }
  get maxDistance() {
    return this.#maxDistance;
  }
  clear() {
  }
  init() {
    this.container.particles.linksColor = void 0;
    this.container.particles.linksColors = /* @__PURE__ */ new Map();
  }
  interact(p1) {
    if (!p1.options.links) {
      return;
    }
    p1.links = [];
    if (p1.linksDistance && p1.linksDistance > this.#maxDistance) {
      this.#maxDistance = p1.linksDistance;
    }
    const pos1 = p1.getPosition(), container = this.container, canvasSize = container.canvas.size;
    if (pos1.x < originPoint.x || pos1.y < originPoint.y || pos1.x > canvasSize.width || pos1.y > canvasSize.height) {
      return;
    }
    const linkOpt1 = p1.options.links, optOpacity = linkOpt1.opacity, optDistance = p1.retina.linksDistance ?? minDistance6, warp = linkOpt1.warp, range = warp ? new CircleWarp(pos1.x, pos1.y, optDistance, canvasSize) : new Circle(pos1.x, pos1.y, optDistance), query = container.particles.grid.query(range);
    for (const p2 of query) {
      const linkOpt2 = p2.options.links;
      if (p1 === p2 || !linkOpt2?.enable || linkOpt1.id !== linkOpt2.id || p2.spawning || p2.destroyed || !p2.links || p1.links.some((t) => t.destination === p2) || p2.links.some((t) => t.destination === p1)) {
        continue;
      }
      const pos2 = p2.getPosition();
      if (pos2.x < originPoint.x || pos2.y < originPoint.y || pos2.x > canvasSize.width || pos2.y > canvasSize.height) {
        continue;
      }
      const distDirect = getDistances(pos1, pos2).distance, distWarp = warp && linkOpt2.warp ? getWarpDistance(pos1, pos2, canvasSize) : distDirect, distance = Math.min(distDirect, distWarp);
      if (distance > optDistance) {
        continue;
      }
      const opacityLine = (opacityOffset - distance / optDistance) * optOpacity;
      this.#setColor(p1);
      p1.links.push({
        destination: p2,
        opacity: opacityLine,
        color: this.#getLinkColor(p1, p2),
        isWarped: distWarp < distDirect
      });
    }
  }
  isEnabled(particle) {
    return !!particle.options.links?.enable;
  }
  loadParticlesOptions(options, ...sources) {
    loadOptionProperty(options, "links", Links, ...sources);
  }
  reset() {
  }
  #getLinkColor(p1, p2) {
    const container = this.container, linksOptions = p1.options.links;
    if (!linksOptions) {
      return;
    }
    const linkColor = linksOptions.id !== void 0 ? container.particles.linksColors.get(linksOptions.id) : container.particles.linksColor;
    return getLinkColor(p1, p2, linkColor);
  }
  #setColor(p1) {
    if (!p1.options.links) {
      return;
    }
    const container = this.container, linksOptions = p1.options.links;
    let linkColor = linksOptions.id === void 0 ? container.particles.linksColor : container.particles.linksColors.get(linksOptions.id);
    if (linkColor) {
      return;
    }
    linkColor = getLinkRandomColor(this.#pluginManager, linksOptions.color, linksOptions.blink, linksOptions.consent);
    if (linksOptions.id === void 0) {
      container.particles.linksColor = linkColor;
    } else {
      container.particles.linksColors.set(linksOptions.id, linkColor);
    }
  }
};

// node_modules/@tsparticles/interaction-particles-links/browser/LinksPlugin.js
var LinksPlugin = class {
  id = "links";
  #pluginManager;
  constructor(pluginManager) {
    this.#pluginManager = pluginManager;
  }
  async getPlugin(container) {
    const { LinkInstance } = await import("./LinkInstance-TAA2DIND.js");
    return new LinkInstance(this.#pluginManager, container);
  }
  loadOptions() {
  }
  needsPlugin() {
    return true;
  }
};

// node_modules/@tsparticles/interaction-particles-links/browser/index.js
async function loadParticlesLinksInteraction(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    const pluginManager = e.pluginManager;
    ensureInteractivityPluginLoaded(e);
    pluginManager.addPlugin(new LinksPlugin(pluginManager));
    pluginManager.addInteractor?.("particlesLinks", (container) => {
      return Promise.resolve(new Linker(pluginManager, container));
    });
  });
}

// node_modules/@tsparticles/shape-polygon/browser/Utils.js
var polygonCache = /* @__PURE__ */ new Map();
var noOffset = 0;
function getUnitPolygon(sides6) {
  const cached = polygonCache.get(sides6);
  if (cached) {
    return cached;
  }
  const step = doublePI / sides6, isOdd = !!(sides6 % double), baseAngle = (-Math.PI + (isOdd ? noOffset : step)) * half, verts = [];
  for (let i = 0; i < sides6; i++) {
    const angle = baseAngle + i * step;
    verts[i] = {
      x: Math.cos(angle),
      y: Math.sin(angle)
    };
  }
  polygonCache.set(sides6, verts);
  return verts;
}
function drawPolygon(data, side) {
  const { context, radius } = data, sides6 = side.count.numerator / side.count.denominator, verts = getUnitPolygon(sides6);
  context.beginPath();
  for (let i = 0; i < verts.length; i++) {
    const vert = verts[i];
    if (!vert) {
      continue;
    }
    const x = vert.x * radius, y = vert.y * radius;
    if (i) {
      context.lineTo(x, y);
    } else {
      context.moveTo(x, y);
    }
  }
  context.closePath();
}

// node_modules/@tsparticles/shape-polygon/browser/PolygonDrawerBase.js
var defaultSides = 5;
var PolygonDrawerBase = class {
  draw(data) {
    const { particle, radius } = data, side = this.getSidesData(particle, radius);
    drawPolygon(data, side);
  }
  getSidesCount(particle) {
    const polygon = particle.shapeData;
    return Math.round(getRangeValue(polygon?.sides ?? defaultSides));
  }
};

// node_modules/@tsparticles/shape-polygon/browser/PolygonDrawer.js
var yFactor = 2.66;
var sidesFactor = 3;
var PolygonDrawer = class extends PolygonDrawerBase {
  getSidesData(particle, radius) {
    const { sides: sides6 } = particle;
    return {
      count: {
        denominator: 1,
        numerator: sides6
      },
      length: radius * yFactor / (sides6 / sidesFactor)
    };
  }
};

// node_modules/@tsparticles/shape-polygon/browser/TriangleDrawer.js
var sides4 = 3;
var yFactor2 = 2.66;
var sidesFactor2 = 3;
var TriangleDrawer = class extends PolygonDrawerBase {
  getSidesCount() {
    return sides4;
  }
  getSidesData(_particle, radius) {
    return {
      count: {
        denominator: 1,
        numerator: sides4
      },
      length: radius * yFactor2 / (sides4 / sidesFactor2)
    };
  }
};

// node_modules/@tsparticles/shape-polygon/browser/index.js
async function loadGenericPolygonShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(["polygon"], () => Promise.resolve(new PolygonDrawer()));
  });
}
async function loadTriangleShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(["triangle"], () => Promise.resolve(new TriangleDrawer()));
  });
}
async function loadPolygonShape(engine) {
  engine.checkVersion("4.3.1");
  await Promise.all([
    loadGenericPolygonShape(engine),
    loadTriangleShape(engine)
  ]);
}

// node_modules/@tsparticles/updater-rotate/browser/Options/Classes/RotateAnimation.js
var RotateAnimation = class {
  decay = 0;
  enable = false;
  speed = 0;
  sync = false;
  load(data) {
    if (isNull(data)) {
      return;
    }
    loadProperty(this, "enable", data.enable);
    loadRangeProperty(this, "speed", data.speed);
    loadRangeProperty(this, "decay", data.decay);
    loadProperty(this, "sync", data.sync);
  }
};

// node_modules/@tsparticles/updater-rotate/browser/Options/Classes/Rotate.js
var Rotate = class extends ValueWithRandom {
  animation = new RotateAnimation();
  direction = RotateDirection.clockwise;
  path = false;
  load(data) {
    if (isNull(data)) {
      return;
    }
    super.load(data);
    loadProperty(this, "direction", data.direction);
    this.animation.load(data.animation);
    loadProperty(this, "path", data.path);
  }
};

// node_modules/@tsparticles/updater-rotate/browser/RotateUpdater.js
var doublePIDeg = 360;
var RotateUpdater = class {
  #container;
  constructor(container) {
    this.#container = container;
  }
  init(particle) {
    const rotateOptions = particle.options.rotate;
    if (!rotateOptions) {
      return;
    }
    particle.rotate = {
      enable: rotateOptions.animation.enable,
      value: degToRad(getRangeValue(rotateOptions.value)),
      min: 0,
      max: doublePI
    };
    particle.pathRotation = rotateOptions.path;
    let rotateDirection = rotateOptions.direction;
    if (rotateDirection === RotateDirection.random) {
      const index = Math.floor(getRandom() * double), minIndex = 0;
      rotateDirection = index > minIndex ? RotateDirection.counterClockwise : RotateDirection.clockwise;
    }
    switch (rotateDirection) {
      case RotateDirection.counterClockwise:
      case "counterClockwise":
        particle.rotate.status = AnimationStatus.decreasing;
        break;
      case RotateDirection.clockwise:
        particle.rotate.status = AnimationStatus.increasing;
        break;
      default:
        break;
    }
    const rotateAnimation = rotateOptions.animation;
    if (rotateAnimation.enable) {
      particle.rotate.decay = identity - getRangeValue(rotateAnimation.decay);
      particle.rotate.velocity = getRangeValue(rotateAnimation.speed) / doublePIDeg * this.#container.retina.reduceFactor;
      if (!rotateAnimation.sync) {
        particle.rotate.velocity *= getRandom();
      }
    }
    particle.rotation = particle.rotate.value;
  }
  isEnabled(particle) {
    const rotate = particle.options.rotate;
    if (!rotate) {
      return false;
    }
    return !particle.destroyed && !particle.spawning && (!!rotate.value || rotate.animation.enable || rotate.path);
  }
  loadOptions(options, ...sources) {
    loadOptionProperty(options, "rotate", Rotate, ...sources);
  }
  update(particle, delta) {
    if (!this.isEnabled(particle)) {
      return;
    }
    particle.isRotating = !!particle.rotate;
    if (!particle.rotate) {
      return;
    }
    updateAnimation(particle, particle.rotate, false, DestroyType.none, delta);
    particle.rotation = particle.rotate.value;
  }
};

// node_modules/@tsparticles/updater-rotate/browser/index.js
async function loadRotateUpdater(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addParticleUpdater("rotate", (container) => {
      return Promise.resolve(new RotateUpdater(container));
    });
  });
}

// node_modules/@tsparticles/shape-square/browser/Utils.js
function drawSquare(data) {
  const { context, radius } = data, fixedRadius = radius * Math.SQRT1_2, fixedDiameter = fixedRadius * double;
  context.rect(-fixedRadius, -fixedRadius, fixedDiameter, fixedDiameter);
}

// node_modules/@tsparticles/shape-square/browser/SquareDrawer.js
var sides5 = 4;
var SquareDrawer = class {
  draw(data) {
    drawSquare(data);
  }
  getSidesCount() {
    return sides5;
  }
};

// node_modules/@tsparticles/shape-square/browser/index.js
async function loadSquareShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(["edge", "square"], () => Promise.resolve(new SquareDrawer()));
  });
}

// node_modules/@tsparticles/shape-star/browser/Utils.js
var defaultInset = 2;
var origin = { x: 0, y: 0 };
function drawStar(data) {
  const { context, particle, radius } = data, sides6 = particle.sides, inset = particle.starInset ?? defaultInset;
  context.moveTo(origin.x, origin.y - radius);
  for (let i = 0; i < sides6; i++) {
    context.rotate(Math.PI / sides6);
    context.lineTo(origin.x, origin.y - radius * inset);
    context.rotate(Math.PI / sides6);
    context.lineTo(origin.x, origin.y - radius);
  }
}

// node_modules/@tsparticles/shape-star/browser/StarDrawer.js
var defaultInset2 = 2;
var defaultSides2 = 5;
var StarDrawer = class {
  draw(data) {
    drawStar(data);
  }
  getSidesCount(particle) {
    const star = particle.shapeData;
    return Math.round(getRangeValue(star?.sides ?? defaultSides2));
  }
  particleInit(_container, particle) {
    const star = particle.shapeData;
    particle.starInset = getRangeValue(star?.inset ?? defaultInset2);
  }
};

// node_modules/@tsparticles/shape-star/browser/index.js
async function loadStarShape(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register((e) => {
    e.pluginManager.addShape(["star"], () => Promise.resolve(new StarDrawer()));
  });
}

// node_modules/@tsparticles/slim/browser/index.js
async function loadSlim(engine) {
  engine.checkVersion("4.3.1");
  await engine.pluginManager.register(async (e) => {
    const loadInteractivityForSlim = async (e2) => {
      await loadInteractivityPlugin(e2);
      await Promise.all([
        loadExternalParallaxInteraction(e2),
        loadExternalAttractInteraction(e2),
        loadExternalBounceInteraction(e2),
        loadExternalBubbleInteraction(e2),
        loadExternalConnectInteraction(e2),
        loadExternalDestroyInteraction(e2),
        loadExternalGrabInteraction(e2),
        loadExternalPauseInteraction(e2),
        loadExternalPushInteraction(e2),
        loadExternalRemoveInteraction(e2),
        loadExternalRepulseInteraction(e2),
        loadExternalSlowInteraction(e2),
        loadParticlesAttractInteraction(e2),
        loadParticlesCollisionsInteraction(e2),
        loadParticlesLinksInteraction(e2)
      ]);
    };
    await Promise.all([
      loadBasic(e),
      loadInteractivityForSlim(e),
      loadEasingQuadPlugin(e),
      loadEmojiShape(e),
      loadImageShape(e),
      loadLineShape(e),
      loadPolygonShape(e),
      loadSquareShape(e),
      loadStarShape(e),
      loadLifeUpdater(e),
      loadPaintUpdater(e),
      loadRotateUpdater(e)
    ]);
  });
}
export {
  loadSlim
};
//# sourceMappingURL=@tsparticles_slim.js.map
