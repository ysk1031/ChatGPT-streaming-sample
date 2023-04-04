import { useEffect, useState } from 'react';

export const useChat: () => {
  text: string;
  error: any | null;
} = () => {
  const [text, setText] = useState<string>('');
  const [error, setError] = useState<any | null>(null);

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
        setError(err);
      });
  }, []);

  return { text, error };
};
