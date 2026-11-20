"""Wires the notice centre into the app: the web API reports every failed paid request, a shortage of credits opens
the top-up window with how many are missing, the notice is mounted in App. Run from the root of the main repo."""


def edit(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


edit('src/credits.ts', [
    ("  topUpOpen: boolean;\n", "  topUpOpen: boolean;\n  /** why the top-up window was opened by a refused generation: credits it needs and credits that are free */\n  topUpNeed: TopUpNeed | null;\n"),
    ("  openTopUp: () => void;\n", "  openTopUp: (need?: TopUpNeed) => void;\n"),
    ("interface CreditsState {", "export interface TopUpNeed { needed: number; available: number; reserved: number }\n\ninterface CreditsState {"),
    ("  topUpOpen: false,\n", "  topUpOpen: false,\n  topUpNeed: null,\n"),
    ("  openTopUp: () => set({ topUpOpen: true }),\n  closeTopUp: () => set({ topUpOpen: false }),",
     "  openTopUp: (need) => set({ topUpOpen: true, topUpNeed: need ?? null }),\n  closeTopUp: () => set({ topUpOpen: false, topUpNeed: null }),"),
])

edit('src/components/TopUpModal.tsx', [
    ("  const { balance, topUpOpen, closeTopUp, refresh } = useCredits();", "  const { balance, topUpOpen, topUpNeed, closeTopUp, refresh } = useCredits();"),
    ("  const openTopUp = useCredits", "  const openTopUp = useCredits") if False else ("  if (!topUpOpen) return null;\n", """  // opened by a generation that was refused for credits: the smallest amount that covers what is missing
  const short = topUpNeed && topUpNeed.needed > topUpNeed.available ? topUpNeed.needed - topUpNeed.available : 0;
  useEffect(() => {
    if (!topUpOpen || short <= 0) return;
    const fit = stops.findIndex((usd) => creditsForTopUp(usd, topup.tiers) >= short);
    setIdx(fit >= 0 ? fit : stops.length - 1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topUpOpen, short]);

  if (!topUpOpen) return null;
"""),
    ("""          <p className="topup-sub">{t.credits.subtitle}</p>
""", """          <p className="topup-sub">{t.credits.subtitle}</p>
          {topUpNeed && (
            <div className="topup-short" role="status">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="12" r="9" />
                <path d="M12 7.500v5.500" />
                <circle cx="12" cy="16.300" r=".600" />
              </svg>
              <div>
                {short > 0 ? (
                  <>
                    <b>{language === 'en' ? `${num(short)} credits short for this generation` : `Для этой генерации не хватает: ${t.credits.count(short)}`}</b>
                    <span>
                      {language === 'en'
                        ? `It needs ${num(topUpNeed.needed)}, ${num(topUpNeed.available)} are free.`
                        : `Нужно ${num(topUpNeed.needed)}, свободно ${num(topUpNeed.available)}.`}
                      {topUpNeed.reserved > 0 &&
                        (language === 'en'
                          ? ` Another ${num(topUpNeed.reserved)} are held by unfinished generations and will be free when they end.`
                          : ` Ещё ${num(topUpNeed.reserved)} заняты незавершёнными генерациями — освободятся, когда они закончатся.`)}
                    </span>
                  </>
                ) : (
                  <>
                    <b>{language === 'en' ? 'Not enough credits for this generation' : 'Для этой генерации не хватает кредитов'}</b>
                    <span>{language === 'en' ? 'Top up the balance and start it again.' : 'Пополните баланс и запустите её снова.'}</span>
                  </>
                )}
              </div>
            </div>
          )}
"""),
    ("import ConsentModal from './ConsentModal';", "import ConsentModal from './ConsentModal';\nimport '../Notices.css';"),
])

edit('src/webApi.ts', [
    ("import { useCredits } from './credits';", "import { useCredits } from './credits';\nimport { reportFailure, type Failure } from './notices';"),
    ("""async function callFunction<T>(name: string, body: unknown, opts: { onJob?: (jobId: string) => void; resumeJob?: string } = {}): Promise<T> {
  const session = await getValidSession();
  if (!session) throw new Error(t().errors.notLoggedIn);
  const kind = TRACKED_FUNCTIONS[name];""", """/** A failed call that already knows what to tell the person (see notices.ts). */
class CallError extends Error {
  constructor(message: string, readonly failure: Failure) {
    super(message);
  }
}

async function callFunction<T>(name: string, body: unknown, opts: { onJob?: (jobId: string) => void; resumeJob?: string } = {}): Promise<T> {
  const kind = TRACKED_FUNCTIONS[name];
  // a price question is asked in the background, many times: its failures are not the person's business
  const quiet = !kind || (body as { action?: unknown } | null)?.action === 'quote';
  const session = await getValidSession();
  if (!session) {
    if (!quiet) reportFailure({ code: 'login' });
    throw new Error(t().errors.notLoggedIn);
  }"""),
    ("    if (kind && res.ok && data == null) throw new Error(t().errors.connectionLost);",
     "    if (kind && res.ok && data == null) throw new CallError(t().errors.connectionLost, { code: 'offline' });"),
    ("      throw new Error(quotaMessage(data) || byCode[data?.code] || data?.error || t().errors.generationError);",
     "      const message = quotaMessage(data) || byCode[data?.code] || data?.error || t().errors.generationError;\n"
     "      const code = res.status === 401 ? 'login' : typeof data?.code === 'string' ? data.code : undefined;\n"
     "      throw new CallError(message, { code, data, message: typeof data?.error === 'string' ? data.error : undefined });"),
    ("""  } catch (err) {
    // The reason is what makes this worth recording: a spike of one failure text is how a
    // broken model or an exhausted provider quota shows up before anyone writes in.
    if (kind) {""", """  } catch (err) {
    // the person is told once, here: the top-up window for a shortage of credits, a notice for the rest
    if (!quiet) reportFailure(err instanceof CallError ? err.failure : err instanceof TypeError ? { code: 'offline' } : { message: err instanceof Error ? err.message : undefined });
    // The reason is what makes this worth recording: a spike of one failure text is how a
    // broken model or an exhausted provider quota shows up before anyone writes in.
    if (kind) {"""),
])

edit('src/App.tsx', [
    ("      <AdminMessageToast />", "      <AdminMessageToast />\n      {IS_WEB && <NoticeCenter />}"),
    ("import AdminMessageToast from", "import NoticeCenter from './components/NoticeCenter';\nimport AdminMessageToast from"),
])

edit('src/notices.ts', [
    ("  const key = f.code ? (SAME[f.code] ?? f.code) : 'failed';",
     "  // a refusal that came as a sentence without a code (a job that failed at the provider)\n"
     "  const told = !f.code && /отклонил|не принимает|по своим правилам|declined|does not accept/i.test(f.message ?? '') ? 'refused' : undefined;\n"
     "  const key = f.code ? (SAME[f.code] ?? f.code) : (told ?? 'failed');"),
])
print('ok')
