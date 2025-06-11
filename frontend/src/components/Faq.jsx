import React from "react";
import "./Faq.css";

const faqData = [
    {
        question: "What is Arvastocks?",
        answer: "Arvastocks is a platform that provides stock market data and analysis tools to help users make informed investment decisions."
    },
    {
        question: "How do I create an account?",
        answer: "You can create an account by clicking on the 'Sign Up' button on the homepage and filling out the registration form."
    },
    {
        question: "How can I modify my profile?",
        answer: "To modify your profile, log in to your account, go to the 'Profile' section, and update your information as needed."
    },
    {
        question: "What features are available on the platform?",
        answer: "Arvastocks offers various features including real-time stock quotes, historical data, news updates, and advanced charting tools."
    },
    {
        question: "How can I contact customer support?",
        answer: "You can contact customer support via email or through the 'Contact Us' form available on the website."
    },
];

export default function Faq() {
  return (
    <div className="about-container">
      <h1 className="faq-title">Frequently Asked Questions</h1>
      <ul className="faq-list">
        {faqData.map((item, idx) => (
          <li key={idx}>
            <strong>{item.question}</strong>
            <p>{item.answer}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}