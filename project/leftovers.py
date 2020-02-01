        if self._id == 'C':
            display.lcd_clear()
            display.lcd_display_string('Ladowanie danych', 1)
            url = requests.get(bruh)
            news = json.loads(url.text)
            wiadomosci = [
                '',
                '',
                '',
                '',
                '',
                '',
                ]
            for i in range(0, 6):
                wiadomosci[i] = news['articles'][i]['title']
            for i in range(0, 6):
                text = spacer + wiadomosci[i]
                for j in range(0, len(text), 4):
                    lcd_text = text[j:j + 16]
                    display.lcd_display_string(lcd_text, 1)
                    time.sleep(0.1)
                    display.lcd_display_string(spacer, 1)
                    is_killed = self._kill.wait(self._interval)
                    if is_killed:
                        display.lcd_clear()
                        break
            self.kill()
