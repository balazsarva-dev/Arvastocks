const faq = [
  ['What is Arvastocks?', 'A free tool for looking at stock prices and the latest news about a company, in one place.'],
  ['Where does the data come from?', 'Prices and news are loaded live from Yahoo Finance. Prices may be delayed by up to 15 minutes.'],
  ['Do I need an account?', 'No. Everything is available without signing up.'],
  ['Is this investment advice?', 'No. Arvastocks only shows publicly available data. Do your own research before investing.'],
  ['How can I reach you?', 'Write to support@arvastocks.com.'],
];

const terms = [
  'The service is provided "as is", without warranty of any kind, including the accuracy or completeness of the data.',
  'We are not liable for any direct or indirect damage resulting from use of the service.',
  'Use the service lawfully; do not misuse, disrupt or try to gain unauthorized access to it.',
  'These terms may change at any time; changes take effect when published here.',
];

export default function About() {
  return (
    <article className="prose">
      <h1>About</h1>
      <p>
        Arvastocks is a passion project by Balazs Arva, a Python developer who enjoys challenges on both
        the backend and the frontend. The goal is simple: give everyone clear, reliable market data so
        they can make better-informed decisions, whether they are seasoned investors or just starting out.
      </p>
      <p>
        Development is ongoing, with new features planned based on feedback and the latest advances in
        data analysis and machine learning.
      </p>

      <h2>FAQ</h2>
      <dl className="faq">
        {faq.map(([q, a]) => (
          <div key={q}>
            <dt>{q}</dt>
            <dd>{a}</dd>
          </div>
        ))}
      </dl>

      <h2>Terms of service</h2>
      <ul>
        {terms.map((t) => (
          <li key={t}>{t}</li>
        ))}
      </ul>

      <p className="muted">
        Questions or feedback? <a href="mailto:support@arvastocks.com">support@arvastocks.com</a>
      </p>
    </article>
  );
}
