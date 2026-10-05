import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import '../fonts';
import { FONT, HAND } from '../fonts';
import { Background } from '../components/Background';
import { Grain } from '../components/Grain';
import { MaskLine } from '../components/MaskLine';
import { C, GRADIENT, TEXT_X, ease, mix, mixRect, prog } from '../theme';
import type { Rect } from '../theme';
import { HAND_VARIANTS, HP_H, HP_W, HandPiece } from './HandPiece';
import type { HandVariant } from './HandPiece';
import { Sketch, rr } from './rough';
import type { Shape } from './rough';

/*
 * ONEFLOW Motion — hand-drawn cut. Same 18 s script and timing as OneflowMotionAd; every line, box,
 * arrow and the cursor are sketched (roughjs) and "boil" on threes; copy is hand-lettered (Caveat).
 *
 *   0– 90  «Идея становится движением» + sketched prompt field: typing, click on «Создать»
 *  72–214  zoom into the workspace: field → «Идея» → «Стиль» → «Моушн», arrows + marker pulse,
 *          «Моушн» opens into the preview
 * 190–350  the generated piece plays  ·  «Типографика. Формы. Движение.»
 * 346–450  preview shrinks, two more variants (paper / blueprint)  ·  «Меньше рутины. Больше идей.»
 * 436–540  end card ONEFLOW MOTION; copy is still from frame 480
 */

const FIELD: Rect = { x: 640, y: 118, w: 534, h: 144, r: 22 };
const CARD_W = 150;
const CARD_GAP = 56;
const CARD_Y = 130;
const CARD_H = 120;
const cardRect = (i: number): Rect => ({ x: 594 + i * (CARD_W + CARD_GAP), y: CARD_Y, w: CARD_W, h: CARD_H, r: 18 });
const CARDS = [cardRect(0), cardRect(1), cardRect(2)];
const CAMERA_ORIGIN = { x: 875, y: 190 };
const ZOOM = 1.07;

const PREVIEW: Rect = { x: 360, y: 28, w: 830, h: 324, r: 22 };
const THUMB_W = (1230 - 2 * TEXT_X - 2 * 20) / 3;
const THUMB_H = (THUMB_W * HP_H) / HP_W;
const THUMB_Y = 154;
const thumb = (i: number): Rect => ({ x: TEXT_X + i * (THUMB_W + 20), y: THUMB_Y, w: THUMB_W, h: THUMB_H, r: 14 });
const FINAL: Rect = { x: 650, y: 84, w: 540, h: (540 * HP_H) / HP_W, r: 18 };

const BUTTON: Rect = { x: FIELD.x + FIELD.w - 18 - 132, y: FIELD.y + FIELD.h - 16 - 46, w: 132, h: 46, r: 23 };
const BTN_C = { x: BUTTON.x + BUTTON.w / 2, y: BUTTON.y + BUTTON.h / 2 };

const PROMPT = 'Создай динамичную анимацию для моего бренда';
const PAPER = '#0F0F13';

const hand = (size: number): CSSProperties => ({
  fontFamily: HAND,
  fontSize: size,
  lineHeight: 1.02,
  fontWeight: 700,
  color: C.ink,
  whiteSpace: 'nowrap',
});

const gradientText: CSSProperties = {
  backgroundImage: GRADIENT,
  WebkitBackgroundClip: 'text',
  backgroundClip: 'text',
  color: 'transparent',
};

/** A sketched box: opaque fill underneath, chalk outline drawn on top. */
const SketchBox: React.FC<{
  rect: Rect;
  frame: number;
  id: number;
  draw?: number;
  stroke?: string;
  strokeWidth?: number;
  fill?: string;
  opacity?: number;
  dx?: number;
  children?: ReactNode;
}> = ({ rect, frame, id, draw = 1, stroke = 'rgba(250,250,250,0.85)', strokeWidth = 1.6, fill = PAPER, opacity = 1, dx = 0, children }) => (
  <div style={{ position: 'absolute', left: rect.x + dx, top: rect.y, width: rect.w, height: rect.h, opacity }}>
    <div style={{ position: 'absolute', inset: 2, borderRadius: rect.r, background: fill, overflow: 'hidden' }}>{children}</div>
    <Sketch
      id={id}
      frame={frame}
      shape={{ kind: 'path', d: rr(1, 1, rect.w - 2, rect.h - 2, rect.r) }}
      draw={draw}
      opts={{ stroke, strokeWidth, roughness: 1.1 }}
    />
  </div>
);

const CardIcon: React.FC<{ kind: number; frame: number; draw: number }> = ({ kind, frame, draw }) => {
  const shapes: { s: Shape; o: object }[] =
    kind === 0
      ? [
          { s: { kind: 'ellipse', cx: 14, cy: 17, w: 20, h: 20 }, o: { stroke: C.ink2, strokeWidth: 1.5 } },
          { s: { kind: 'ellipse', cx: 26, cy: 6, w: 8, h: 8 }, o: { stroke: C.blue, fill: C.blue, fillStyle: 'solid' } },
        ]
      : kind === 1
        ? [
            { s: { kind: 'ellipse', cx: 12, cy: 16, w: 18, h: 18 }, o: { stroke: C.blue, fill: C.blue, fillStyle: 'hachure', hachureGap: 3 } },
            { s: { kind: 'ellipse', cx: 22, cy: 16, w: 18, h: 18 }, o: { stroke: C.violet, fill: C.violet, fillStyle: 'hachure', hachureAngle: 40, hachureGap: 3 } },
          ]
        : [
            { s: { kind: 'path', d: rr(2, 9, 30, 14, 7) }, o: { stroke: C.ink2, strokeWidth: 1.5 } },
            { s: { kind: 'ellipse', cx: 10, cy: 16, w: 8, h: 8 }, o: { stroke: C.violet, fill: C.violet, fillStyle: 'solid' } },
          ];
  return (
    <div style={{ position: 'absolute', right: 14, top: 12, width: 34, height: 30 }}>
      {shapes.map(({ s, o }, i) => (
        <Sketch key={i} id={300 + kind * 4 + i} frame={frame} shape={s} draw={draw} opts={{ strokeWidth: 1.4, roughness: 1, ...o }} />
      ))}
    </div>
  );
};

const CardFace: React.FC<{ index: number; title: string; frame: number; opacity: number; lit: number; done: number }> = ({
  index,
  title,
  frame,
  opacity,
  lit,
  done,
}) => (
  <div style={{ position: 'absolute', inset: 0, opacity }}>
    <div style={{ position: 'absolute', left: 16, top: 10, fontFamily: HAND, fontSize: 22, color: C.ink3 }}>0{index + 1}</div>
    <CardIcon kind={index} frame={frame} draw={1} />
    <div style={{ position: 'absolute', left: 16, bottom: 18, ...hand(36), color: lit > 0.3 ? '#fff' : C.ink }}>{title}</div>
    <div style={{ position: 'absolute', left: 14, bottom: 10, width: 100, height: 10 }}>
      <Sketch
        id={320 + index}
        frame={frame}
        shape={{ kind: 'curve', pts: [[0, 6], [40, 3], [96, 5]] }}
        draw={done}
        opts={{ stroke: C.blue, strokeWidth: 3.5, roughness: 0.9 }}
      />
    </div>
  </div>
);

const HandWindow: React.FC<{
  rect: Rect;
  frame: number;
  id: number;
  t: number;
  v: HandVariant;
  pieceOpacity: number;
  chrome: number;
  opacity?: number;
  draw?: number;
  lit?: number;
  seed?: number;
  children?: ReactNode;
}> = ({ rect, frame, id, t, v, pieceOpacity, chrome, opacity = 1, draw = 1, lit = 0, seed, children }) => {
  const s = Math.max(rect.w / HP_W, rect.h / HP_H);
  const edge = 1 - chrome;
  const maskX = `linear-gradient(90deg, rgba(0,0,0,${1 - edge}) 0%, #000 ${edge * 18}%, #000 ${100 - edge * 6}%, rgba(0,0,0,${1 - edge}) 100%)`;
  const maskY = `linear-gradient(180deg, rgba(0,0,0,${1 - edge}) 0%, #000 ${edge * 14}%, #000 ${100 - edge * 14}%, rgba(0,0,0,${1 - edge}) 100%)`;
  return (
    <div style={{ position: 'absolute', left: rect.x, top: rect.y, width: rect.w, height: rect.h, opacity }}>
      <div
        style={{
          position: 'absolute',
          inset: 2,
          borderRadius: rect.r,
          overflow: 'hidden',
          background: `rgba(15,15,19,${chrome})`,
          boxShadow: `0 30px 70px -34px rgba(59,123,255,${0.45 * chrome})`,
        }}
      >
        <div style={{ position: 'absolute', inset: 0, WebkitMaskImage: maskX, maskImage: maskX }}>
          <div style={{ position: 'absolute', inset: 0, WebkitMaskImage: maskY, maskImage: maskY }}>
            <div
              style={{
                position: 'absolute',
                left: (rect.w - 4 - HP_W * s) / 2,
                top: (rect.h - 4 - HP_H * s) / 2,
                width: HP_W,
                height: HP_H,
                transform: `scale(${s})`,
                transformOrigin: '0 0',
                opacity: pieceOpacity,
              }}
            >
              <HandPiece t={t} frame={frame} v={v} bgOpacity={chrome} seed={seed} />
            </div>
          </div>
        </div>
        {children}
      </div>
      <div style={{ position: 'absolute', inset: 0, opacity: chrome }}>
        <Sketch
          id={id}
          frame={frame}
          shape={{ kind: 'path', d: rr(1, 1, rect.w - 2, rect.h - 2, rect.r) }}
          draw={draw}
          opts={{ stroke: lit > 0.2 ? C.blueSoft : 'rgba(250,250,250,0.8)', strokeWidth: 1.6 + lit * 1.2, roughness: 1.1 }}
        />
      </div>
    </div>
  );
};

export const HandAd: React.FC = () => {
  const f = useCurrentFrame();

  // ---- camera ---------------------------------------------------------------------------------------
  const zoom = mix(mix(1, ZOOM, prog(f, 76, 140, ease.inOut)), 1, prog(f, 176, 214, ease.inOut));
  const camera: CSSProperties = {
    position: 'absolute',
    inset: 0,
    transform: `scale(${zoom})`,
    transformOrigin: `${CAMERA_ORIGIN.x}px ${CAMERA_ORIGIN.y}px`,
  };

  // ---- scene 1 --------------------------------------------------------------------------------------
  const fieldDraw = prog(f, 2, 24, ease.soft);
  const fieldIn = prog(f, 0, 8);
  const chars = Math.floor(interpolate(f, [12, 52], [0, PROMPT.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const caretOn = f < 56 || Math.floor(f / 8) % 2 === 0;
  const press = f < 58 ? 0 : f < 61 ? prog(f, 58, 61, ease.soft) : 1 - prog(f, 61, 68, ease.out);
  const scribble = prog(f, 58, 70, ease.out);
  const scribbleOut = prog(f, 80, 92);
  const sparks = prog(f, 60, 72, ease.out);
  const sparksOut = prog(f, 70, 84);
  const toCard = prog(f, 72, 104, ease.inOut);
  const fieldRect = mixRect(FIELD, CARDS[0], toCard);
  const fieldContent = 1 - prog(f, 68, 78);

  const cursorMove = prog(f, 28, 56, ease.inOut);
  const cur = {
    x: mix(1150, BTN_C.x + 8, cursorMove) + prog(f, 66, 86) * 14,
    y: mix(352, BTN_C.y + 4, cursorMove) + prog(f, 66, 86) * 12,
    s: 1 - press * 0.14,
    o: prog(f, 26, 34) * (1 - prog(f, 74, 86)),
  };

  // ---- scene 2 --------------------------------------------------------------------------------------
  const cardIn = [1, prog(f, 98, 122), prog(f, 110, 134)];
  const cardDraw = [1, prog(f, 98, 120, ease.soft), prog(f, 110, 132, ease.soft)];
  const arrowDraw = [prog(f, 112, 128, ease.inOut), prog(f, 126, 142, ease.inOut)];
  const pulseP = prog(f, 140, 178, ease.soft);
  const pulseX = mix(CARDS[0].x + CARD_W / 2, CARDS[2].x + CARD_W / 2, pulseP);
  const pulseOn = prog(f, 138, 144) * (1 - prog(f, 176, 186));
  const lit = CARDS.map((c) => Math.max(0, 1 - Math.abs(pulseX - (c.x + CARD_W / 2)) / 110) * pulseOn);
  const done = CARDS.map((c, i) => prog(f, 140 + i * 17, 150 + i * 17, ease.out));
  const arrowLit = [0, 1].map((i) => {
    const a = CARDS[i].x + CARD_W;
    return interpolate(pulseX, [a, a + CARD_GAP], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  });
  const chainOut = prog(f, 176, 194, ease.inOut);

  // ---- «Моушн» → preview → thumb → end card ---------------------------------------------------------
  const open = prog(f, 176, 214, ease.inOut);
  const shrink = prog(f, 346, 376, ease.inOut);
  const settle = prog(f, 444, 484, ease.inOut);
  let mainRect = mixRect(CARDS[2], PREVIEW, open);
  if (f >= 346) mainRect = mixRect(PREVIEW, thumb(1), shrink);
  if (f >= 444) mainRect = mixRect(thumb(1), FINAL, settle);
  const mainChrome = 1 - prog(f, 462, 500, ease.soft);
  const tA = f - 190;

  const varOut = prog(f, 370, 398, ease.out);
  const varBack = prog(f, 436, 458, ease.inOut);
  const varOpacity = prog(f, 370, 382) * (1 - prog(f, 436, 452));
  const varRect = (slot: number) => mixRect(mixRect(thumb(1), thumb(slot), varOut), thumb(1), varBack);

  // ---- copy -----------------------------------------------------------------------------------------
  const t1 = [0, 1].map((i) => ({ enter: prog(f, i * 5, 22 + i * 5), exit: prog(f, 78 + i * 3, 92 + i * 3, ease.inOut) }));
  const t2 = [0, 1].map((i) => ({ enter: prog(f, 90 + i * 6, 112 + i * 6), exit: prog(f, 180 + i * 3, 194 + i * 3, ease.inOut) }));
  const t3 = [0, 1, 2].map((i) => ({ enter: prog(f, 214 + i * 8, 236 + i * 8), exit: prog(f, 330 + i * 3, 344 + i * 3, ease.inOut) }));
  const t4 = { enter: prog(f, 362, 382), exit: prog(f, 446, 460, ease.inOut) };
  const t5 = [prog(f, 458, 476), prog(f, 462, 478), prog(f, 466, 480)];

  const focusX = interpolate(f, [0, 90, 210, 360, 450, 540], [900, 880, 760, 640, 900, 920], { extrapolateRight: 'clamp' });

  const underline = (id: number, w: number, draw: number, color = C.blue) => (
    <div style={{ position: 'relative', width: w, height: 14, marginTop: -6 }}>
      <Sketch
        id={id}
        frame={f}
        shape={{ kind: 'curve', pts: [[2, 9], [w * 0.35, 4], [w * 0.7, 8], [w - 2, 3]] }}
        draw={draw}
        opts={{ stroke: color, strokeWidth: 4.5, roughness: 1 }}
      />
    </div>
  );

  return (
    <AbsoluteFill style={{ fontFamily: FONT, overflow: 'hidden', backgroundColor: C.bg }}>
      <Background frame={f} focusX={focusX} />

      {/* ================= workspace (inside the camera) ================= */}
      <div style={camera}>
        {/* arrows between the cards, re-inked in blue as the pulse runs through */}
        {[0, 1].map((i) => {
          const x1 = CARDS[i].x + CARD_W + 6;
          const x2 = CARDS[i + 1].x - 8;
          const y = CARD_Y + CARD_H / 2;
          const arrow = (color: string, draw: number, id: number, w: number) => (
            <>
              <Sketch id={id} frame={f} shape={{ kind: 'curve', pts: [[x1, y + 2], [(x1 + x2) / 2, y - 9], [x2, y]] }} draw={draw} opts={{ stroke: color, strokeWidth: w, roughness: 0.8 }} />
              <Sketch id={id + 1} frame={f} shape={{ kind: 'line', x1: x2 - 9, y1: y - 7, x2, y2: y }} draw={prog(draw, 0.8, 1, ease.soft)} opts={{ stroke: color, strokeWidth: w, roughness: 0.6 }} />
              <Sketch id={id + 2} frame={f} shape={{ kind: 'line', x1: x2 - 9, y1: y + 7, x2, y2: y }} draw={prog(draw, 0.85, 1, ease.soft)} opts={{ stroke: color, strokeWidth: w, roughness: 0.6 }} />
            </>
          );
          return (
            <div key={i} style={{ position: 'absolute', inset: 0, opacity: 1 - chainOut }}>
              {arrow('rgba(250,250,250,0.7)', arrowDraw[i], 200 + i * 10, 1.6)}
              {arrowLit[i] > 0 && arrow(C.blueSoft, arrowLit[i], 205 + i * 10, 2.6)}
            </div>
          );
        })}

        {/* marker dot travelling along the chain (hidden behind the cards) */}
        <div style={{ position: 'absolute', left: pulseX - 9, top: CARD_Y + CARD_H / 2 - 12, width: 18, height: 18, opacity: pulseOn, filter: 'drop-shadow(0 0 8px rgba(127,168,255,0.9))' }}>
          <Sketch id={240} frame={f} shape={{ kind: 'ellipse', cx: 9, cy: 9, w: 16, h: 16 }} opts={{ stroke: '#fff', strokeWidth: 1.2, fill: C.blueSoft, fillStyle: 'solid' }} />
        </div>

        <SketchBox
          rect={CARDS[1]}
          frame={f}
          id={110}
          draw={cardDraw[1]}
          stroke={lit[1] > 0.2 ? C.blueSoft : undefined}
          strokeWidth={1.6 + lit[1] * 1.2}
          opacity={prog(f, 98, 106) * (1 - chainOut)}
          dx={mix(-24, 0, cardIn[1]) - chainOut * 30}
        >
          <CardFace index={1} title="Стиль" frame={f} opacity={prog(f, 106, 120)} lit={lit[1]} done={done[1]} />
        </SketchBox>

        {/* card 1 is the prompt field itself */}
        <SketchBox
          rect={fieldRect}
          frame={f}
          id={100}
          draw={fieldDraw}
          stroke={lit[0] > 0.2 ? C.blueSoft : undefined}
          strokeWidth={1.6 + lit[0] * 1.2}
          opacity={fieldIn * (1 - chainOut)}
          dx={-chainOut * 30}
        >
          <div style={{ position: 'absolute', inset: 0, opacity: fieldContent }}>
            <div style={{ position: 'absolute', left: 20, top: 12, display: 'flex', alignItems: 'center', gap: 8, fontFamily: HAND, fontSize: 22, color: C.ink3 }}>
              <div style={{ position: 'relative', width: 10, height: 10 }}>
                <Sketch id={120} frame={f} shape={{ kind: 'ellipse', cx: 5, cy: 5, w: 9, h: 9 }} opts={{ stroke: C.blue, fill: C.blue, fillStyle: 'solid', strokeWidth: 1 }} />
              </div>
              опиши идею
            </div>
            <div style={{ position: 'absolute', left: 20, top: 44, width: 494, ...hand(31), fontWeight: 400, whiteSpace: 'normal', lineHeight: '34px' }}>
              {PROMPT.slice(0, chars)}
              <span style={{ display: 'inline-block', width: 3, height: 28, marginLeft: 3, verticalAlign: '-5px', borderRadius: 2, background: C.blueSoft, opacity: caretOn ? 1 : 0 }} />
            </div>
          </div>
          <CardFace index={0} title="Идея" frame={f} opacity={prog(f, 94, 108)} lit={lit[0]} done={done[0]} />
        </SketchBox>

        {/* «Создать» button + click scribble + sparks (inside the camera, above the field) */}
        <div style={{ position: 'absolute', inset: 0, opacity: fieldIn * fieldContent }}>
          <div
            style={{
              position: 'absolute',
              left: BUTTON.x,
              top: BUTTON.y,
              width: BUTTON.w,
              height: BUTTON.h,
              transform: `scale(${1 - press * 0.07})`,
            }}
          >
            <div style={{ position: 'absolute', inset: 3, borderRadius: 99, background: `linear-gradient(90deg, ${C.blue}, #6F6BFF)`, opacity: 0.85 }} />
            <Sketch
              id={130}
              frame={f}
              shape={{ kind: 'path', d: rr(1, 1, BUTTON.w - 2, BUTTON.h - 2, BUTTON.r) }}
              draw={prog(f, 10, 26, ease.soft)}
              opts={{ stroke: '#fff', strokeWidth: 1.6, fill: '#9FC0FF', fillStyle: 'hachure', hachureGap: 7, fillWeight: 1, roughness: 1 }}
            />
            <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', ...hand(28), color: '#fff' }}>
              Создать →
            </div>
          </div>
          <div style={{ position: 'absolute', left: BTN_C.x - 92, top: BTN_C.y - 40, width: 184, height: 80, opacity: 1 - scribbleOut }}>
            <Sketch id={140} frame={f} shape={{ kind: 'ellipse', cx: 92, cy: 40, w: 178, h: 72 }} draw={scribble} opts={{ stroke: C.violet, strokeWidth: 2.6, roughness: 1.6 }} />
          </div>
          {[-150, -110, -70, -30, 20, 200].map((deg, i) => {
            const a = (deg * Math.PI) / 180;
            const r0 = 102;
            const r1 = mix(r0, r0 + 22, sparks);
            return (
              <div key={i} style={{ position: 'absolute', inset: 0, opacity: (1 - sparksOut) * (sparks > 0 ? 1 : 0) }}>
                <Sketch
                  id={150 + i}
                  frame={f}
                  shape={{ kind: 'line', x1: BTN_C.x + Math.cos(a) * r0, y1: BTN_C.y + Math.sin(a) * r0 * 0.5, x2: BTN_C.x + Math.cos(a) * r1, y2: BTN_C.y + Math.sin(a) * r1 * 0.5 }}
                  opts={{ stroke: i % 2 ? C.blueSoft : C.violet, strokeWidth: 2.4, roughness: 0.6 }}
                />
              </div>
            );
          })}
        </div>

        {f >= 110 && f < 444 && (
          <HandWindow
            rect={{ ...mainRect, x: mainRect.x + mix(-24, 0, cardIn[2]) }}
            frame={f}
            id={160}
            t={tA}
            v={HAND_VARIANTS.a}
            pieceOpacity={prog(f, 188, 204)}
            chrome={1}
            opacity={prog(f, 110, 118)}
            draw={cardDraw[2]}
            lit={Math.max(lit[2], prog(f, 168, 176) * (1 - prog(f, 180, 196)))}
          >
            <div style={{ position: 'absolute', inset: 0, background: PAPER, opacity: 1 - prog(f, 182, 198) }}>
              <CardFace index={2} title="Моушн" frame={f} opacity={prog(f, 118, 132) * (1 - prog(f, 176, 186))} lit={lit[2]} done={done[2]} />
            </div>
            {/* pencil playhead line */}
            <div style={{ position: 'absolute', left: 24, right: 24, bottom: 10, height: 10, opacity: prog(f, 206, 222) * (1 - prog(f, 338, 350)) }}>
              <Sketch id={170} frame={f} shape={{ kind: 'line', x1: 0, y1: 5, x2: 778, y2: 5 }} opts={{ stroke: 'rgba(255,255,255,0.25)', strokeWidth: 1.2 }} />
              <Sketch id={171} frame={f} shape={{ kind: 'line', x1: 0, y1: 5, x2: 778, y2: 5 }} draw={prog(f, 192, 346, (x) => x)} opts={{ stroke: C.blueSoft, strokeWidth: 2.4 }} />
            </div>
          </HandWindow>
        )}

        {f >= 370 && f < 456 && (
          <>
            <HandWindow rect={varRect(0)} frame={f} id={180} t={(f - 370) + 18} v={HAND_VARIANTS.b} pieceOpacity={1} chrome={1} opacity={varOpacity} seed={500} />
            <HandWindow rect={varRect(2)} frame={f} id={190} t={(f - 370) + 26} v={HAND_VARIANTS.c} pieceOpacity={1} chrome={1} opacity={varOpacity} seed={700} />
          </>
        )}
        {f >= 444 && <HandWindow rect={mainRect} frame={f} id={160} t={tA} v={HAND_VARIANTS.a} pieceOpacity={1} chrome={mainChrome} />}

        {/* sketched cursor */}
        {cur.o > 0 && (
          <div style={{ position: 'absolute', left: cur.x - 3, top: cur.y - 2, width: 30, height: 34, opacity: cur.o, transform: `scale(${cur.s})`, transformOrigin: '3px 2px', filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.6))' }}>
            <Sketch
              id={260}
              frame={f}
              shape={{ kind: 'polygon', pts: [[3, 2], [3, 25], [9, 19], [13.5, 29], [18, 27], [13.6, 17.6], [22, 17.6]] }}
              opts={{ stroke: '#09090B', strokeWidth: 1.6, fill: '#FAFAFA', fillStyle: 'solid', roughness: 0.7 }}
            />
          </div>
        )}
      </div>

      {/* ================= copy ================= */}
      <div style={{ position: 'absolute', left: TEXT_X, top: 104 }}>
        <MaskLine enter={t1[0].enter} exit={t1[0].exit}>
          <div style={hand(64)}>Идея становится</div>
        </MaskLine>
        <MaskLine enter={t1[1].enter} exit={t1[1].exit}>
          <div style={{ ...hand(64), ...gradientText }}>движением</div>
        </MaskLine>
        <div style={{ opacity: 1 - t1[1].exit }}>{underline(400, 250, prog(f, 22, 36, ease.out))}</div>
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 118 }}>
        <MaskLine enter={t2[0].enter} exit={t2[0].exit}>
          <div style={hand(56)}>Задай направление.</div>
        </MaskLine>
        <MaskLine enter={t2[1].enter} exit={t2[1].exit}>
          <div style={{ ...hand(56), ...gradientText }}>Запусти создание.</div>
        </MaskLine>
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 120 }}>
        {['Типографика.', 'Формы.', 'Движение.'].map((w, i) => (
          <MaskLine key={w} enter={t3[i].enter} exit={t3[i].exit}>
            <div style={{ ...hand(28), lineHeight: '44px', ...(i === 2 ? gradientText : {}) }}>{w}</div>
          </MaskLine>
        ))}
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 36 }}>
        <MaskLine enter={t4.enter} exit={t4.exit}>
          <div style={hand(56)}>
            Меньше рутины. <span style={gradientText}>Больше идей.</span>
          </div>
        </MaskLine>
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 112 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 18 }}>
          <MaskLine enter={t5[0]}>
            <span style={{ fontFamily: FONT, fontSize: 64, lineHeight: 1.08, fontWeight: 600, letterSpacing: '-0.04em', color: C.ink }}>ONEFLOW</span>
          </MaskLine>
          <MaskLine enter={t5[1]} style={{ paddingRight: 12, marginRight: -12 }}>
            <span style={{ ...hand(64), lineHeight: 1.08, paddingRight: 6, ...gradientText }}>MOTION</span>
          </MaskLine>
        </div>
        {underline(410, 300, prog(f, 470, 480, ease.out), C.violet)}
        <MaskLine enter={t5[2]} style={{ marginTop: 10 }}>
          <div style={{ ...hand(28), color: C.ink2 }}>Моушн-графика — быстро и удобно</div>
        </MaskLine>
      </div>

      <Grain frame={f} />
    </AbsoluteFill>
  );
};
