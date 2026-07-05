async def _receive_audio(self):
    print('[BUDDY] 👂 Recv started')
    out_buf, in_buf = ([], [])
    try:
        while True:
            async for response in self.session.receive():
                if response.data:
                    if self._turn_done_event and self._turn_done_event.is_set():
                        self._turn_done_event.clear()
                    self.audio_in_queue.put_nowait(response.data)
                if response.server_content:
                    sc = response.server_content
                    if sc.output_transcription and sc.output_transcription.text:
                        txt = _clean_transcript(sc.output_transcription.text)
                        if txt:
                            out_buf.append(txt)
                    if sc.input_transcription and sc.input_transcription.text:
                        txt = _clean_transcript(sc.input_transcription.text)
                        if txt:
                            in_buf.append(txt)
                    if sc.turn_complete:
                        if self._turn_done_event:
                            self._turn_done_event.set()
                        full_in = ' '.join(in_buf).strip()
                        if full_in:
                            self.ui.write_log(f'You: {full_in}')
                            if self._dashboard:
                                asyncio.create_task(self._dashboard.broadcast({'type': 'log', 'speaker': 'user', 'text': full_in, 'ts': datetime.now().isoformat()}))
                        in_buf = []
                        full_out = ' '.join(out_buf).strip()
                        if full_out:
                            self.ui.write_log(f'Buddy: {full_out}')
                            if self._dashboard:
                                asyncio.create_task(self._dashboard.broadcast({'type': 'log', 'speaker': 'buddy', 'text': full_out, 'ts': datetime.now().isoformat()}))
                        out_buf = []
                if response.tool_call:
                    fn_responses = []
                    for fc in response.tool_call.function_calls:
                        print(f'[BUDDY] 📞 {fc.name}')
                        fr = await self._execute_tool(fc)
                        fn_responses.append(fr)
                    await self.session.send_tool_response(function_responses=fn_responses)
    except Exception as e:
        print(f'[BUDDY] ❌ Recv: {e}')
        traceback.print_exc()
        raise