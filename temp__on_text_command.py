def _on_text_command(self, text: str):
    if not self._loop or not self.session:
        return
    asyncio.run_coroutine_threadsafe(self.session.send_client_content(turns={'parts': [{'text': text}]}, turn_complete=True), self._loop)