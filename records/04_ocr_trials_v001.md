# records/04 · OCR trials on 天方至聖實錄 (1924), page 10 (preface p. 3) · v001

Reference (read from the page image, column 1):
朝夕矣。惟憾塵絆。假抄未竟。丙申冬。忽幸金陵景初袁老夫子下訪。示書命弁展

| Run | Engine / method | Output, column 1 |
|---|---|---|
| DO001[1] | tesseract chi_tra --psm 5 (vertical block) | unusable (mixed Latin noise) |
| DO001[2] | tesseract jpn_vert --psm 5 | 朝 実 瓜 燃 塵 朝 便 抄 未 意 滞 申 多 多幸 金 農 景 初 勅 老 夫 子 下 該 示 書 |
| DO001[3] | columns cut into cells, laid out as one horizontal line, tesseract chi_tra --psm 7 | 朝夕痰。惟協卒絆,假抄未胃申和父。忽幸金鑒景初品老夫子下訪示點 |
| DO001[4] | as [3], ring punctuation removed first | 朝夕炎惟居塵彌假擱未竟丙申冬怨幸金鑒景共齊老夫子下苗示書 |
| DO001[5] | as [4], each cell alone, --psm 10 | 井夕志。惟壇塵肥。假抄以竟。丙皿金。急□金中景守齊老夫子下咐。示書人 |
| DO001[6] | as [4], RapidOCR PP-OCRv3 (line height 48) | 朝夕突惟鹰辩假抄未竞丙串冬忽幸金陵景初袁老夫子下訪示書人 |

Result: best ≈ 75–85 % of characters, and simplified forms appear (竞, 鹰). Not faithful enough.
Decision (user, 21 Nov 2026): copy the pages as they are; add only a cover and copyright page.
© Computational Classnotes · CC BY-NC-SA 4.0
