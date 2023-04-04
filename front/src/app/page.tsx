'use client';
import { useChat } from './hooks/useChat';
import styles from './page.module.css';

export default function Home() {
  const { text } = useChat();

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
