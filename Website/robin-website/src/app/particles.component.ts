import { Component, ElementRef, OnInit, OnDestroy, AfterViewInit, ViewChild } from '@angular/core';

interface Firefly {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
  opacitySpeed: number;
  hue: number;
  glowRadius: number;
  glowSpeed: number;
  glowDir: number;
}

@Component({
  selector: 'app-particles',
  standalone: true,
  imports: [],
  template: `<canvas #fireflyCanvas class="firefly-canvas"></canvas>`,
  styles: [`
    :host {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
    }
    .firefly-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  `]
})
export class ParticlesComponent implements AfterViewInit, OnDestroy {
  @ViewChild('fireflyCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  private ctx!: CanvasRenderingContext2D;
  private fireflies: Firefly[] = [];
  private animationId!: number;
  private resizeObserver!: ResizeObserver;

  ngAfterViewInit(): void {
    const canvas = this.canvasRef.nativeElement;
    this.ctx = canvas.getContext('2d')!;
    this.resizeCanvas();
    this.createFireflies(120);
    this.animate();

    this.resizeObserver = new ResizeObserver(() => {
      this.resizeCanvas();
    });
    this.resizeObserver.observe(document.body);
  }

  ngOnDestroy(): void {
    cancelAnimationFrame(this.animationId);
    if (this.resizeObserver) this.resizeObserver.disconnect();
  }

  private resizeCanvas(): void {
    const canvas = this.canvasRef.nativeElement;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  private createFireflies(count: number): void {
    this.fireflies = [];
    for (let i = 0; i < count; i++) {
      this.fireflies.push(this.createFirefly());
    }
  }

  private createFirefly(): Firefly {
    const canvas = this.canvasRef.nativeElement;
    const hues = [45, 55, 180, 200, 280]; // gold, amber, cyan, blue, purple
    return {
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      radius: Math.random() * 2.5 + 0.8,
      opacity: Math.random() * 0.5 + 0.1,
      opacitySpeed: Math.random() * 0.006 + 0.002,
      hue: hues[Math.floor(Math.random() * hues.length)] + Math.random() * 20 - 10,
      glowRadius: Math.random() * 8 + 4,
      glowSpeed: Math.random() * 0.03 + 0.01,
      glowDir: Math.random() > 0.5 ? 1 : -1,
    };
  }

  private animate(): void {
    const canvas = this.canvasRef.nativeElement;
    const ctx = this.ctx;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const f of this.fireflies) {
      // Update position
      f.x += f.vx;
      f.y += f.vy;

      // Drift slightly for organic motion
      f.vx += (Math.random() - 0.5) * 0.04;
      f.vy += (Math.random() - 0.5) * 0.04;
      f.vx = Math.max(-0.8, Math.min(0.8, f.vx));
      f.vy = Math.max(-0.8, Math.min(0.8, f.vy));

      // Wrap around edges
      if (f.x < 0) f.x = canvas.width;
      if (f.x > canvas.width) f.x = 0;
      if (f.y < 0) f.y = canvas.height;
      if (f.y > canvas.height) f.y = 0;

      // Pulse opacity
      f.opacity += f.opacitySpeed;
      if (f.opacity > 0.9 || f.opacity < 0.05) {
        f.opacitySpeed *= -1;
      }

      // Pulse glow
      f.glowRadius += f.glowSpeed * f.glowDir;
      if (f.glowRadius > 18 || f.glowRadius < 4) {
        f.glowDir *= -1;
      }

      // Draw glow aura
      const glow = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.glowRadius * 3);
      glow.addColorStop(0, `hsla(${f.hue}, 100%, 70%, ${f.opacity * 0.8})`);
      glow.addColorStop(0.4, `hsla(${f.hue}, 100%, 60%, ${f.opacity * 0.3})`);
      glow.addColorStop(1, `hsla(${f.hue}, 100%, 50%, 0)`);

      ctx.beginPath();
      ctx.arc(f.x, f.y, f.glowRadius * 3, 0, Math.PI * 2);
      ctx.fillStyle = glow;
      ctx.fill();

      // Draw core dot
      ctx.beginPath();
      ctx.arc(f.x, f.y, f.radius, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${f.hue}, 100%, 90%, ${Math.min(1, f.opacity * 1.5)})`;
      ctx.shadowBlur = f.glowRadius * 2;
      ctx.shadowColor = `hsl(${f.hue}, 100%, 70%)`;
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    this.animationId = requestAnimationFrame(() => this.animate());
  }
}
