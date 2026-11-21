(* ::Package:: *)
(* HanKitabKernel v001 : Wolfram Cloud chat proxy for the Han Kitab reader (HanKitab_v001.html).
   Same design and protocol as TUTUKernel / LaplacianLabKernel (CCN Cloud Kit):
     POST key, mode ("wolfram" | "chat"), code_b64, payload_b64  ->  JSON
     mode "wolfram": evaluates code, returns text, text_b64, image, chat_ready
     mode "chat":    payload_b64 = base64(UTF-8 JSON {model, max_tokens, system, messages})
                     returns text_b64 and stop_reason, or error and status. The chat key is never returned.
   Run these two steps from a signed-in Mathematica or Wolfram Cloud notebook (the Claude Wolfram
   connector is not signed in to the Cloud, so it cannot deploy).
   (c) Computational Classnotes . CC BY-NC-SA 4.0 *)

(* Step 1, once: store the chat API key privately in your cloud account *)
CloudPut["PASTE-THE-CHAT-API-KEY-HERE", "HanKitab/apikey", Permissions -> "Private"]

(* Step 2: deploy. Choose a long secret: it is the "CCN Cloud key" typed into the app.
   Deploying again under the same name keeps the URL:
   https://www.wolframcloud.com/obj/ccn2/HanKitabKernel *)
With[{keyObj = CloudObject["HanKitab/apikey"], secret = "CHOOSE-A-LONG-SECRET"},
 CloudDeploy[
  APIFunction[
   {"code" -> "String" -> "", "code_b64" -> "String" -> "", "key" -> "String",
    "mode" -> "String" -> "wolfram", "payload_b64" -> "String" -> ""},
   Module[{b64s, fromB64, chatCall, chat, code},
    b64s[s_String] := BaseEncode[StringToByteArray[s]];
    fromB64[b_String] := Quiet@Check[ByteArrayToString[BaseDecode[b]], ""];
    chatCall[payload_String, apiKey_String] := Module[{p, model, resp, body, status},
      p = Quiet@Check[ImportByteArray[StringToByteArray[payload], "RawJSON"], $Failed];
      If[! AssociationQ[p] || ! ListQ[p["messages"]], Return[<|"error" -> "bad payload", "status" -> 400|>]];
      model = Replace[p["model"], Except[_String?(StringStartsQ["claude-"])] -> "claude-sonnet-5-5"];
      resp = URLRead[HTTPRequest["https://api.anthropic.com/v1/messages", <|"Method" -> "POST",
          "Headers" -> {"x-api-key" -> apiKey, "anthropic-version" -> "2023-06-01", "content-type" -> "application/json"},
          "Body" -> ExportByteArray[DeleteMissing@<|"model" -> model,
              "max_tokens" -> Clip[Replace[p["max_tokens"], Except[_Integer] -> 1500], {1, 4096}],
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
    chat = Quiet@Check[CloudGet[keyObj], ""];
    chat = If[StringQ[chat], StringTrim[chat], ""];
    Which[
     #key =!= secret,
      Failure["Forbidden", <|"Message" -> "bad key"|>],
     #mode === "chat",
      If[chat === "", <|"error" -> "no chat key stored", "status" -> 503|>,
       chatCall[fromB64[#["payload_b64"]], chat]],
     True,
      code = If[#["code_b64"] =!= "", fromB64[#["code_b64"]], #code];
      Module[{r = TimeConstrained[ToExpression[code], 60, $Aborted], img, txt},
       img = If[FreeQ[r, _Graphics | _Graphics3D | _Image | _Legended], "",
         BaseEncode[ExportByteArray[Rasterize[r, ImageResolution -> 110], "PNG"]]];
       txt = ToString[r /. g : (_Graphics | _Graphics3D | _Image | _Legended) :> "-Graphics-", InputForm];
       <|"text" -> txt, "text_b64" -> b64s[txt], "image" -> img, "chat_ready" -> chat =!= ""|>]
     ]] &,
   "JSON"],
  "HanKitabKernel", Permissions -> "Public"]]

(* Step 3, check (from the notebook): should give {version, 2} and chat_ready -> True *)
(* URLExecute["https://www.wolframcloud.com/obj/ccn2/HanKitabKernel",
     {"key" -> "CHOOSE-A-LONG-SECRET", "code" -> "{$VersionNumber, 1 + 1}"}, "RawJSON", Method -> "POST"] *)
