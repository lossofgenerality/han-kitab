(* ::Package:: *)
(* HanKitabKernel v002 : Wolfram Cloud chat proxy for the Han Kitab reader (HanKitab_v001.html).
   Same design and protocol as TUTUKernel / LaplacianLabKernel (CCN Cloud Kit):
     POST key, mode ("wolfram" | "chat"), code_b64, payload_b64  ->  JSON
     mode "status":  no key needed; returns chat_ready and open_chat
     mode "chat":    no key needed (open to readers; v002); max_tokens capped at 1500, at most 12 messages
     mode "wolfram": needs the secret; evaluates code, returns text, text_b64, chat_ready
     mode "chat":    payload_b64 = base64(UTF-8 JSON {model, max_tokens, system, messages})
                     returns text_b64 and stop_reason, or error and status. The chat key is never returned.
   Run these two steps from a signed-in Mathematica or Wolfram Cloud notebook (the Claude Wolfram
   connector is not signed in to the Cloud, so it cannot deploy).
   (c) Computational Classnotes . CC BY-NC-SA 4.0 *)

(* Step 1, once: store the chat API key privately in your cloud account.
   Until HanKitab/apikey exists the kernel falls back to LaplacianLab/apikey. *)
CloudPut["PASTE-THE-CHAT-API-KEY-HERE", "HanKitab/apikey", Permissions -> "Private"]

(* Step 2: deploy. The secret only guards the "wolfram" mode (code evaluation), for the owner.
   v002: secret = CloudGet["HanKitab/secret"].
   Deploying again under the same name keeps the URL:
   https://www.wolframcloud.com/obj/ccn2/HanKitabKernel *)
With[{keyObjs = {CloudObject["HanKitab/apikey"], CloudObject["LaplacianLab/apikey"]}, secret = CloudGet["HanKitab/secret"]},
 CloudDeploy[
  APIFunction[
   {"code" -> "String" -> "", "code_b64" -> "String" -> "", "key" -> "String" -> "",
    "mode" -> "String" -> "status", "payload_b64" -> "String" -> ""},
   Module[{b64s, fromB64, chatCall, chat, code},
    b64s[s_String] := BaseEncode[StringToByteArray[s]];
    fromB64[b_String] := Quiet@Check[ByteArrayToString[BaseDecode[b]], ""];
    chatCall[payload_String, apiKey_String] := Module[{p, model, resp, body, status},
      p = Quiet@Check[ImportByteArray[StringToByteArray[payload], "RawJSON"], $Failed];
      If[! AssociationQ[p] || ! ListQ[p["messages"]] || Length[p["messages"]] > 12 || StringLength[payload] > 60000,
       Return[<|"error" -> "bad payload", "status" -> 400|>]];
      model = Replace[p["model"], Except[_String?(StringStartsQ["claude-"])] -> "claude-sonnet-5-5"];
      resp = URLRead[HTTPRequest["https://api.anthropic.com/v1/messages", <|"Method" -> "POST",
          "Headers" -> {"x-api-key" -> apiKey, "anthropic-version" -> "2023-06-01", "content-type" -> "application/json"},
          "Body" -> ExportByteArray[DeleteMissing@<|"model" -> model,
              "max_tokens" -> Clip[Replace[p["max_tokens"], Except[_Integer] -> 1500], {1, 1500}],
              "system" -> p["system"], "messages" -> p["messages"]|>, "RawJSON", "Compact" -> True]|>],
        TimeConstraint -> 110];
      If[FailureQ[resp], Return[<|"error" -> "chat service unreachable", "status" -> 502|>]];
      status = resp["StatusCode"];
      body = Quiet@Check[ImportByteArray[resp["BodyByteArray"], "RawJSON"], <||>];
      If[status === 200 && AssociationQ[body],
       <|"text_b64" -> b64s@StringJoin[Cases[Lookup[body, "content", {}],
            KeyValuePattern[{"type" -> "text", "text" -> t_String}] :> t]],
         "stop_reason" -> Lookup[body, "stop_reason", ""]|>,
       <|"error" -> If[AssociationQ[body], Lookup[Lookup[body, "error", <||>], "message", "chat request failed"], "chat request failed"],
         "status" -> status|>]];
    chat = "";
    Do[If[chat === "", chat = Quiet@Check[CloudGet[o], ""]; chat = If[StringQ[chat], StringTrim[chat], ""]], {o, keyObjs}];
    Which[
     #mode === "status", <|"chat_ready" -> chat =!= "", "open_chat" -> True|>,
     #mode === "chat",
      If[chat === "", <|"error" -> "no chat key stored", "status" -> 503|>,
       chatCall[fromB64[#["payload_b64"]], chat]],
     #key =!= secret,
      Failure["Forbidden", <|"Message" -> "bad key"|>],
     True,
      code = If[#["code_b64"] =!= "", fromB64[#["code_b64"]], #code];
      Module[{r = TimeConstrained[ToExpression[code], 60, $Aborted], txt},
       txt = ToString[r, InputForm];
       <|"text" -> txt, "text_b64" -> b64s[txt], "chat_ready" -> chat =!= ""|>]
     ]] &,
   "JSON"],
  "HanKitabKernel", Permissions -> "Public"]]

(* Step 3, check: mode "status" needs no key and should give chat_ready -> True, open_chat -> True *)
