'use client';
import { useStreamChat } from './hooks/useStreamChat';
import styles from './page.module.css';

export default function Home() {
  const userPrompt = '有事に強い組織とはどういった組織でしょうか？';
  const { text } = useStreamChat(userPrompt);

  return (
    <main className={styles.main}>
      <h3 style={{ marginBottom: '24px' }}>{userPrompt}</h3>
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
