# records/10 · kernel notebook tests, 21 Nov 2026

Problem in HanKitabKernel_v002.nb: the test cell used u and secret defined in another cell, and the Chinese question was UTF-8 encoded twice (ExportString then StringToByteArray).
Fix (T046): HanKitabKernel_v003.nb, each test cell self-contained, payload made with ExportByteArray.

| Run | Cell | Result |
|---|---|---|
| DO012[1] | status | chat_ready True, open_chat True ✔ |
| DO012[2] | chat, "Who wrote 天方性理?" | end_turn, 《天方性理》由清代回族穆斯林学者刘智(刘介廉)所著。 ✔ |
| DO012[3] | code with secret | {15., 2} ✔ |

© Computational Classnotes · CC BY-NC-SA 4.0
