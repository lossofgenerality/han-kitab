# records/05 · HanKitabKernel tests · v001 (21 Nov 2026)

Deployed: https://www.wolframcloud.com/obj/ccn2/HanKitabKernel (Permissions -> "Public", secret-gated;
chat key read from the private object LaplacianLab/apikey; secret stored privately as HanKitab/secret).

| Run | Request | Result |
|---|---|---|
| DO006[1] | key = wrong, code 1+1 | Success False, Failure[Forbidden, bad key] ✔ |
| DO006[2] | key = secret, code {$VersionNumber, 1 + 1} | text "{15., 2}", chat_ready True ✔ |
| DO006[3] | mode chat, max_tokens 60, "Who wrote 天方性理?" | stop_reason max_tokens, empty text ✘ |
| DO006[4] | same, max_tokens 1500 | end_turn: "《天方性理》(Tianfang Xingli) was written by the Qing-dynasty Chinese Muslim scholar Liu Zhi (劉智)." ✔ |

Fix from [3]: the app sends max_tokens 1500 (was 900).
© Computational Classnotes · CC BY-NC-SA 4.0
