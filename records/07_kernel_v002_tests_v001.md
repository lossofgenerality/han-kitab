# records/07 · HanKitabKernel v002 tests (21 Nov 2026)

| Run | Request | Result |
|---|---|---|
| DO009[1] | mode status, no key | chat_ready True, open_chat True ✔ |
| DO009[2] | mode wolfram, code 1+1, no key | refused (bad key) ✔ |
| DO009[3] | mode wolfram, code 1+1, secret | "2" ✔ |
| DO009[4] | mode chat, no key, "Who wrote 天方至聖實錄?" | answer received ✔ |

Chat key: HanKitab/apikey when stored, otherwise LaplacianLab/apikey.

© Computational Classnotes · CC BY-NC-SA 4.0
