'use client';
import { useEffect, useState } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [text, setText] = useState<string>('');

  useEffect(() => {
    fetch('http://localhost:8000/streaming_chat', {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      headers: {
        Accept: 'text/event-stream',
      },
    })
      .then((response) => {
        const body = response.body;
        const reader = body!.getReader();
        const decoder = new TextDecoder('utf-8');

        const stream = new ReadableStream({
          start(controller) {
            let pump: () => void = () => {
              return reader.read().then(({ done, value }) => {
                // データを消費する必要がなくなったら、ストリームを閉じる
                if (done) {
                  controller.close();
                  return;
                }

                // ストリームで渡ってきた文字の一部を取り出しstate更新
                let dataString = decoder.decode(value);
                setText((prev) => prev + dataString);

                // 次のデータチャンクを対象のストリームのキューに入れる
                controller.enqueue(value);
                return pump();
              });
            };

            return pump();
          },
        });
        return stream;
      })
      .then((stream) => {
        const newRes = new Response(stream);
        return newRes.text();
      })
      .then((text) => {
        setText(text);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <main className={styles.main}>
      <h3 style={{ marginBottom: '24px' }}>
        AI時代を危惧したラップを披露してください。
      </h3>
      <div style={{ maxHeight: '480px', maxWidth: '480px' }}>
        {text.split('\n').map((elem, i) => (
          <p key={i} style={{ marginTop: 0, marginBottom: '8px' }}>
            {elem}
          </p>
        ))}
      </div>
    </main>
  );
}
