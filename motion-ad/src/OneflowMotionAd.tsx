import type { CSSProperties, ReactNode } from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import './fonts';
import { FONT } from './fonts';
import { Background } from './components/Background';
import { Cursor } from './components/Cursor';
import { Grain } from './components/Grain';
import { MaskLine } from './components/MaskLine';
import { MotionPiece, PIECE_H, PIECE_W, VARIANTS } from './components/MotionPiece';
import type { Variant } from './components/MotionPiece';
import { CardFace, Panel, PROMPT, PromptContent } from './components/Workspace';
import { C, GRADIENT, TEXT_X, ease, mix, mixRect, prog } from './theme';
import type { Rect } from './theme';

/*
 * ONEFLOW Motion — 18 s, 1230×380, 30 fps, silent.
 *
 *   0– 90  «Идея становится движением» + prompt field: typing, click on «Создать»
 *  72–214  zoom into the workspace: field → «Идея» → «Стиль» → «Моушн», lines + light pulse,
 *          «Моушн» opens into the preview window
 * 190–350  the generated motion piece plays in the preview  ·  «Типографика. Формы. Движение.»
 * 346–450  preview shrinks, two more variants (palette / layout / rhythm)  ·  «Меньше рутины. Больше идей.»
 * 436–540  everything gathers into the end card: ONEFLOW MOTION; text is still from frame 480
 */

// ---- geometry (workspace coordinates; the camera transforms them) ---------------------------------
const FIELD: Rect = { x: 640, y: 118, w: 534, h: 144, r: 20 };
const CARD_W = 160;
const CARD_GAP = 40;
const CARD_Y = 130;
const CARD_H = 120;
const cardRect = (i: number): Rect => ({ x: 594 + i * (CARD_W + CARD_GAP), y: CARD_Y, w: CARD_W, h: CARD_H, r: 18 });
const CARDS = [cardRect(0), cardRect(1), cardRect(2)];
const CAMERA_ORIGIN = { x: 874, y: 190 };
const ZOOM = 1.07;

const PREVIEW: Rect = { x: 360, y: 28, w: 830, h: 324, r: 22 };
const THUMB_W = (1230 - 2 * TEXT_X - 2 * 20) / 3;
const THUMB_H = (THUMB_W * PIECE_H) / PIECE_W;
const THUMB_Y = 154;
const thumb = (i: number): Rect => ({ x: TEXT_X + i * (THUMB_W + 20), y: THUMB_Y, w: THUMB_W, h: THUMB_H, r: 14 });
const FINAL: Rect = { x: 650, y: 84, w: 540, h: (540 * PIECE_H) / PIECE_W, r: 18 };

// button centre inside the field
const BUTTON = { x: FIELD.x + FIELD.w - 16 - 58, y: FIELD.y + FIELD.h - 16 - 20 };

const headline: CSSProperties = {
  fontSize: 60,
  lineHeight: 1.08,
  fontWeight: 500,
  letterSpacing: '-0.035em',
  color: C.ink,
  whiteSpace: 'nowrap',
};

const gradientText: CSSProperties = {
  backgroundImage: GRADIENT,
  WebkitBackgroundClip: 'text',
  backgroundClip: 'text',
  color: 'transparent',
};

/** A composed piece placed inside a rect: scaled to cover it, clipped to its rounded corners. */
const PieceWindow: React.FC<{
  rect: Rect;
  t: number;
  v: Variant;
  pieceOpacity: number;
  chrome: number;
  glow?: number;
  opacity?: number;
  children?: ReactNode;
}> = ({ rect, t, v, pieceOpacity, chrome, glow = 0, opacity = 1, children }) => {
  const s = Math.max(rect.w / PIECE_W, rect.h / PIECE_H);
  // when the chrome fades (end card) the piece melts into the background through soft edges
  const edge = 1 - chrome;
  const maskX = `linear-gradient(90deg, rgba(0,0,0,${1 - edge}) 0%, #000 ${edge * 18}%, #000 ${100 - edge * 6}%, rgba(0,0,0,${1 - edge}) 100%)`;
  const maskY = `linear-gradient(180deg, rgba(0,0,0,${1 - edge}) 0%, #000 ${edge * 14}%, #000 ${100 - edge * 14}%, rgba(0,0,0,${1 - edge}) 100%)`;
  return (
    <div
      style={{
        position: 'absolute',
        left: rect.x,
        top: rect.y,
        width: rect.w,
        height: rect.h,
        borderRadius: rect.r,
        opacity,
        boxShadow: [
          `0 0 0 1px rgba(255,255,255,${0.12 * chrome + 0.3 * glow})`,
          `0 30px 70px -34px rgba(59,123,255,${0.45 * chrome})`,
        ].join(', '),
        overflow: 'hidden',
        background: `rgba(14,15,20,${chrome})`,
      }}
    >
      <div style={{ position: 'absolute', inset: 0, WebkitMaskImage: maskX, maskImage: maskX }}>
        <div style={{ position: 'absolute', inset: 0, WebkitMaskImage: maskY, maskImage: maskY }}>
          <div
            style={{
              position: 'absolute',
              left: (rect.w - PIECE_W * s) / 2,
              top: (rect.h - PIECE_H * s) / 2,
              width: PIECE_W,
              height: PIECE_H,
              transform: `scale(${s})`,
              transformOrigin: '0 0',
              opacity: pieceOpacity,
            }}
          >
            <MotionPiece t={t} v={v} bgOpacity={chrome} />
          </div>
        </div>
      </div>
      {children}
    </div>
  );
};

export const OneflowMotionAd: React.FC = () => {
  const f = useCurrentFrame();

  // ---- camera: push into the workspace, then back out as the preview opens -------------------------
  const zoom = mix(mix(1, ZOOM, prog(f, 76, 140, ease.inOut)), 1, prog(f, 176, 214, ease.inOut));
  const camera: CSSProperties = {
    position: 'absolute',
    inset: 0,
    transform: `scale(${zoom})`,
    transformOrigin: `${CAMERA_ORIGIN.x}px ${CAMERA_ORIGIN.y}px`,
  };

  // ---- scene 1: prompt -------------------------------------------------------------------------------
  const fieldIn = prog(f, 2, 26);
  const chars = Math.floor(interpolate(f, [12, 52], [0, PROMPT.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const caretOn = f < 56 || Math.floor(f / 8) % 2 === 0;
  const press = f < 58 ? 0 : f < 61 ? prog(f, 58, 61, ease.soft) : 1 - prog(f, 61, 68, ease.out);
  const ripple = f < 60 ? 0 : prog(f, 60, 86, ease.out);
  const fieldGlow = prog(f, 59, 64) * (1 - prog(f, 82, 108));
  const toCard = prog(f, 72, 104, ease.inOut);
  const fieldRect = mixRect(FIELD, CARDS[0], toCard);

  const cursorMove = prog(f, 28, 56, ease.inOut);
  const cursor = {
    x: mix(1150, BUTTON.x - 4, cursorMove) + prog(f, 66, 86) * 14,
    y: mix(352, BUTTON.y - 2, cursorMove) + prog(f, 66, 86) * 12,
    scale: 1 - press * 0.14,
    opacity: prog(f, 26, 34) * (1 - prog(f, 74, 86)),
  };

  // ---- scene 2: chain of cards ----------------------------------------------------------------------
  const cardIn = [1, prog(f, 98, 122), prog(f, 110, 134)];
  const lineDraw = [prog(f, 108, 126, ease.inOut), prog(f, 122, 140, ease.inOut)];
  const pulseP = prog(f, 140, 178, ease.soft);
  const pulseX = mix(CARDS[0].x + CARD_W / 2, CARDS[2].x + CARD_W / 2, pulseP);
  const pulseOn = prog(f, 138, 144) * (1 - prog(f, 176, 186));
  const lit = CARDS.map((c, i) => {
    const near = Math.max(0, 1 - Math.abs(pulseX - (c.x + CARD_W / 2)) / 120) * pulseOn;
    return i === 2 ? Math.max(near, prog(f, 168, 178) * (1 - prog(f, 180, 196))) : near;
  });
  const chainOut = prog(f, 176, 194, ease.inOut);

  // ---- «Моушн» → preview → thumbnail → end card ------------------------------------------------------
  const open = prog(f, 176, 214, ease.inOut);
  const shrink = prog(f, 346, 376, ease.inOut);
  const settle = prog(f, 444, 484, ease.inOut);
  let mainRect = mixRect(CARDS[2], PREVIEW, open);
  if (f >= 346) mainRect = mixRect(PREVIEW, thumb(1), shrink);
  if (f >= 444) mainRect = mixRect(thumb(1), FINAL, settle);
  const mainChrome = 1 - prog(f, 462, 500, ease.soft);
  const tA = f - 190;

  // the two extra variants come out from behind the main preview and go back into it
  const varOut = prog(f, 370, 398, ease.out);
  const varBack = prog(f, 436, 458, ease.inOut);
  const varOpacity = prog(f, 370, 382) * (1 - prog(f, 436, 452));
  const varRect = (slot: number) => mixRect(mixRect(thumb(1), thumb(slot), varOut), thumb(1), varBack);

  // ---- copy ------------------------------------------------------------------------------------------
  const t1 = [0, 1].map((i) => ({ enter: prog(f, i * 5, 22 + i * 5), exit: prog(f, 78 + i * 3, 92 + i * 3, ease.inOut) }));
  const t2 = [0, 1].map((i) => ({ enter: prog(f, 90 + i * 6, 112 + i * 6), exit: prog(f, 180 + i * 3, 194 + i * 3, ease.inOut) }));
  const t3 = [0, 1, 2].map((i) => ({ enter: prog(f, 214 + i * 8, 236 + i * 8), exit: prog(f, 330 + i * 3, 344 + i * 3, ease.inOut) }));
  const t4 = { enter: prog(f, 362, 382), exit: prog(f, 446, 460, ease.inOut) };
  const t5 = [prog(f, 458, 476), prog(f, 462, 478), prog(f, 466, 480)];

  const focusX = interpolate(f, [0, 90, 210, 360, 450, 540], [900, 880, 760, 640, 900, 920], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ fontFamily: FONT, overflow: 'hidden', backgroundColor: C.bg }}>
      <Background frame={f} focusX={focusX} />

      {/* ============ workspace (inside the camera) ============ */}
      <div style={camera}>
        {/* connectors + light pulse (behind the cards, visible in the gaps) */}
        {[0, 1].map((i) => {
          const x1 = CARDS[i].x + CARD_W;
          return (
            <div key={i} style={{ opacity: 1 - chainOut }}>
              <div
                style={{
                  position: 'absolute',
                  left: x1,
                  top: CARD_Y + CARD_H / 2,
                  width: CARD_GAP,
                  height: 1,
                  background: 'rgba(255,255,255,0.3)',
                  transform: `scaleX(${lineDraw[i]})`,
                  transformOrigin: 'left',
                }}
              />
              {[x1, x1 + CARD_GAP].map((x, k) => (
                <div
                  key={k}
                  style={{
                    position: 'absolute',
                    left: x - 3,
                    top: CARD_Y + CARD_H / 2 - 3,
                    width: 6,
                    height: 6,
                    borderRadius: 9,
                    background: C.bg,
                    boxShadow: `inset 0 0 0 1px ${C.ink3}`,
                    opacity: prog(lineDraw[i], k * 0.7, k * 0.7 + 0.3, ease.soft),
                  }}
                />
              ))}
            </div>
          );
        })}
        <div
          style={{
            position: 'absolute',
            left: pulseX - 90,
            top: CARD_Y + CARD_H / 2 - 1,
            width: 180,
            height: 2,
            opacity: pulseOn,
            background: `linear-gradient(90deg, transparent, ${C.blueSoft}, #fff, ${C.violet}, transparent)`,
            filter: 'drop-shadow(0 0 6px rgba(127,168,255,0.9))',
          }}
        />

        {/* card 2 «Стиль» and card 3 «Моушн» (card 3 becomes the preview) */}
        <Panel rect={CARDS[1]} glow={lit[1]} opacity={cardIn[1] * (1 - chainOut)} dx={mix(-24, 0, cardIn[1]) - chainOut * 30}>
          <CardFace index={1} title="Стиль" opacity={1} lit={lit[1]} />
        </Panel>

        {/* card 1: the prompt field itself shrinks into «Идея» */}
        <Panel rect={fieldRect} glow={Math.max(fieldGlow, lit[0])} opacity={fieldIn * (1 - chainOut)} dx={mix(40, 0, fieldIn) - chainOut * 30}>
          <PromptContent chars={chars} caretOn={caretOn} press={press} ripple={ripple} opacity={1 - prog(f, 70, 80)} />
          <CardFace index={0} title="Идея" opacity={prog(f, 94, 108)} lit={lit[0]} />
        </Panel>

        {f >= 110 && f < 444 && (
          <PieceWindow
            rect={{ ...mainRect, x: mainRect.x + mix(-24, 0, cardIn[2]) }}
            t={tA}
            v={VARIANTS.a}
            pieceOpacity={prog(f, 188, 204)}
            chrome={1}
            glow={lit[2]}
            opacity={cardIn[2]}
          >
            <div style={{ position: 'absolute', inset: 0, background: '#111115', opacity: 1 - prog(f, 182, 198) }}>
              <CardFace index={2} title="Моушн" opacity={1 - prog(f, 176, 186)} lit={lit[2]} />
            </div>
            {/* thin playback line of the preview */}
            <div
              style={{
                position: 'absolute',
                left: 24,
                right: 24,
                bottom: 14,
                height: 1,
                background: 'rgba(255,255,255,0.14)',
                opacity: prog(f, 206, 222) * (1 - prog(f, 338, 350)),
              }}
            >
              <div style={{ width: `${prog(f, 192, 346, (x) => x) * 100}%`, height: 1, background: GRADIENT }} />
            </div>
          </PieceWindow>
        )}

        {/* the two extra variants */}
        {f >= 370 && f < 456 && (
          <>
            <PieceWindow rect={varRect(0)} t={(f - 370) * 1 + 18} v={VARIANTS.b} pieceOpacity={1} chrome={1} opacity={varOpacity} />
            <PieceWindow rect={varRect(2)} t={(f - 370) * 1 + 26} v={VARIANTS.c} pieceOpacity={1} chrome={1} opacity={varOpacity} />
          </>
        )}
        {f >= 444 && <PieceWindow rect={mainRect} t={tA} v={VARIANTS.a} pieceOpacity={1} chrome={mainChrome} />}

        {cursor.opacity > 0 && <Cursor {...cursor} />}
      </div>

      {/* ============ copy (outside the camera, so it stays still and sharp) ============ */}
      <div style={{ position: 'absolute', left: TEXT_X, top: 122 }}>
        <MaskLine enter={t1[0].enter} exit={t1[0].exit}>
          <div style={headline}>Идея становится</div>
        </MaskLine>
        <MaskLine enter={t1[1].enter} exit={t1[1].exit}>
          <div style={{ ...headline, ...gradientText }}>движением</div>
        </MaskLine>
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 134 }}>
        <MaskLine enter={t2[0].enter} exit={t2[0].exit}>
          <div style={{ ...headline, fontSize: 48 }}>Задай направление.</div>
        </MaskLine>
        <MaskLine enter={t2[1].enter} exit={t2[1].exit}>
          <div style={{ ...headline, fontSize: 48, ...gradientText }}>Запусти создание.</div>
        </MaskLine>
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 128 }}>
        {['Типографика.', 'Формы.', 'Движение.'].map((w, i) => (
          <MaskLine key={w} enter={t3[i].enter} exit={t3[i].exit}>
            <div style={{ ...headline, fontSize: 28, lineHeight: '42px', letterSpacing: '-0.02em', ...(i === 2 ? gradientText : {}) }}>{w}</div>
          </MaskLine>
        ))}
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 46 }}>
        <MaskLine enter={t4.enter} exit={t4.exit}>
          <div style={{ ...headline, fontSize: 48 }}>
            Меньше рутины. <span style={gradientText}>Больше идей.</span>
          </div>
        </MaskLine>
      </div>

      <div style={{ position: 'absolute', left: TEXT_X, top: 126 }}>
        <div style={{ display: 'flex', gap: '0.26em', ...headline, fontSize: 64, fontWeight: 600, letterSpacing: '-0.04em' }}>
          <MaskLine enter={t5[0]}>
            <span>ONEFLOW</span>
          </MaskLine>
          <MaskLine enter={t5[1]}>
            <span style={{ ...gradientText, fontWeight: 300 }}>MOTION</span>
          </MaskLine>
        </div>
        <MaskLine enter={t5[2]} style={{ marginTop: 18 }}>
          <div style={{ fontSize: 26, lineHeight: 1.3, color: C.ink2, letterSpacing: '-0.01em', whiteSpace: 'nowrap' }}>
            Моушн-графика — быстро и удобно
          </div>
        </MaskLine>
      </div>

      <Grain frame={f} />
    </AbsoluteFill>
  );
};
