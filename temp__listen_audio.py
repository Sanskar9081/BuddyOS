async def _listen_audio(self):
    print('[BUDDY] 🎤 Mic started')
    loop = asyncio.get_event_loop()

    def callback(indata, frames, time_info, status):
        with self._speaking_lock:
            buddy_speaking = self._is_speaking
        if not buddy_speaking and (not self.ui.muted) and (not self._phone_active):
            data = indata.tobytes()
            loop.call_soon_threadsafe(self.out_queue.put_nowait, {'data': data, 'mime_type': 'audio/pcm'})
    try:
        with sd.InputStream(samplerate=SEND_SAMPLE_RATE, channels=CHANNELS, dtype='int16', blocksize=CHUNK_SIZE, callback=callback):
            print('[BUDDY] 🎤 Mic stream open')
            while True:
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f'[BUDDY] ❌ Mic: {e}')
        raise