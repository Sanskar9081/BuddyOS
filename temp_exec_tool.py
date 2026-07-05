async def _execute_tool(self, fc) -> types.FunctionResponse:
    name = fc.name
    args = dict(fc.args or {})
    print(f'[BUDDY] 🔧 {name}  {args}')
    self.ui.set_state('THINKING')
    if name == 'save_memory':
        category = args.get('category', 'notes')
        key = args.get('key', '')
        value = args.get('value', '')
        if key and value:
            update_memory({category: {key: {'value': value}}})
            print(f'[Memory] 💾 save_memory: {category}/{key} = {value}')
        if not self.ui.muted:
            self.ui.set_state('LISTENING')
        return types.FunctionResponse(id=fc.id, name=name, response={'result': 'ok', 'silent': True})
    loop = asyncio.get_event_loop()
    result = 'Done.'
    try:
        if name == 'open_app':
            r = await loop.run_in_executor(None, lambda: open_app(parameters=args, response=None, player=self.ui))
            result = r or f"Opened {args.get('app_name')}."
        elif name == 'weather_report':
            r = await loop.run_in_executor(None, lambda: weather_action(parameters=args, player=self.ui))
            result = r or 'Weather delivered.'
        elif name == 'browser_control':
            r = await loop.run_in_executor(None, lambda: browser_control(parameters=args, player=self.ui))
            result = r or 'Done.'
        elif name == 'file_controller':
            r = await loop.run_in_executor(None, lambda: file_controller(parameters=args, player=self.ui))
            result = r or 'Done.'
        elif name == 'send_message':
            r = await loop.run_in_executor(None, lambda: send_message(parameters=args, response=None, player=self.ui, session_memory=None))
            result = r or f"Message sent to {args.get('receiver')}."
        elif name == 'reminder':
            r = await loop.run_in_executor(None, lambda: reminder(parameters=args, response=None, player=self.ui))
            result = r or 'Reminder set.'
        elif name == 'youtube_video':
            r = await loop.run_in_executor(None, lambda: youtube_video(parameters=args, response=None, player=self.ui))
            result = r or 'Done.'
        elif name == 'screen_process':
            threading.Thread(target=screen_process, kwargs={'parameters': args, 'response': None, 'player': self.ui, 'session_memory': None}, daemon=True).start()
            result = 'Vision module activated. Stay completely silent — vision module will speak directly.'
        elif name == 'computer_settings':
            r = await loop.run_in_executor(None, lambda: computer_settings(parameters=args, response=None, player=self.ui))
            result = r or 'Done.'
        elif name == 'desktop_control':
            r = await loop.run_in_executor(None, lambda: desktop_control(parameters=args, player=self.ui))
            result = r or 'Done.'
        elif name == 'code_helper':
            r = await loop.run_in_executor(None, lambda: code_helper(parameters=args, player=self.ui, speak=self.speak))
            result = r or 'Done.'
        elif name == 'dev_agent':
            r = await loop.run_in_executor(None, lambda: dev_agent(parameters=args, player=self.ui, speak=self.speak))
            result = r or 'Done.'
        elif name == 'web_search':
            r = await loop.run_in_executor(None, lambda: web_search_action(parameters=args, player=self.ui))
            result = r or 'Done.'
            if r and len(r) > 120:
                mode = args.get('mode', 'search').upper()
                query = args.get('query') or ', '.join(args.get('items', []))
                label = f'{mode} — {query[:38]}' if query else mode
                self.ui.show_content(label, r)
        elif name == 'file_processor':
            if not args.get('file_path') and self.ui.current_file:
                args['file_path'] = self.ui.current_file
            r = await loop.run_in_executor(None, lambda: file_processor(parameters=args, player=self.ui, speak=self.speak))
            result = r or 'Done.'
        elif name == 'computer_control':
            r = await loop.run_in_executor(None, lambda: computer_control(parameters=args, player=self.ui))
            result = r or 'Done.'
        elif name == 'game_updater':
            r = await loop.run_in_executor(None, lambda: game_updater(parameters=args, player=self.ui, speak=self.speak))
            result = r or 'Done.'
        elif name == 'flight_finder':
            r = await loop.run_in_executor(None, lambda: flight_finder(parameters=args, player=self.ui))
            result = r or 'Done.'
        elif name == 'system_status':
            r = await loop.run_in_executor(None, get_system_status)
            result = str(r)
        elif name == 'shutdown_buddy':
            self.ui.write_log('SYS: Shutdown requested.')
            self.speak('Goodbye, sir.')

            def _shutdown():
                import time, os
                time.sleep(1)
                os._exit(0)
            threading.Thread(target=_shutdown, daemon=True).start()
        else:
            result = f'Unknown tool: {name}'
    except Exception as e:
        result = f"Tool '{name}' failed: {e}"
        traceback.print_exc()
        self.speak_error(name, e)
    if not self.ui.muted:
        self.ui.set_state('LISTENING')
    print(f'[BUDDY] 📤 {name} → {str(result)[:80]}')
    return types.FunctionResponse(id=fc.id, name=name, response={'result': result})