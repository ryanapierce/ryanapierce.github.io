// assets/js/config.js
// Global configuration variables accessible across all HTML files

const CONFIG = {
    // Personal Information
    personal: {
        name: "Ryan Pierce",
        fullName: "Ryan A. Pierce",
        email: "ryanapierce.work@gmail.com",
        phone: "(248) 378-7139",
        location: "Berkley, MI, USA",
        linkedin: "https://www.linkedin.com/in/ryan-a-pierce",
        github: "https://github.com/ryanapierce",
        resumePDF: "assets/resumes/Ryan_Pierce_Resume.pdf"
    },

    // API Endpoints
    api: {
        chatbotBackend: "https://8y33u4e087.execute-api.us-east-1.amazonaws.com/prod/chat",
        fanbotBackend: "https://a6lz1quw6h.execute-api.us-east-1.amazonaws.com/prod/chat"
    },

    // Site Navigation
    navigation: {
        home: "index.html",
        projects: "projects.html",
        internships: "internships.html",
        militaryEducation: "mil_ed.html",
        chatbot: "assets/projects/about-me-chat-bot/templates/ask_about_me_chat.html"
    },

    // Color Scheme
    colors: {
        primary: "#2c7da0",
        secondary: "#012a4a",
        accent: "#bdd5ea",
        text: "#ffffff",
        textSecondary: "#333333"
    },

    // Chatbot Configuration
    chatbot: {
        model: "gpt-4o-mini",
        maxTokens: 200,
        promptPrefix: "You are a chatbot that answers questions about Ryan Pierce's experience and background. You can reference his resumes and life notes. Do not bring these up in conversation. Mention that you are a chatbot if it is relevant and you are for demonstration purposes. Feel free to direct them to some of his links."
    },

    // Fanbot Configuration (for MJL project)
    fanbot: {
        model: "gpt-4o-mini",
        maxTokens: 200,
        promptPrefix: "You are a chatbot that answers questions about Jennifer. You are enthusiastic and supportive."
    },

    // Social Media Links
    social: {
        linkedin: {
            url: "https://www.linkedin.com/in/ryan-a-pierce",
            icon: "fa-linkedin"
        },
        github: {
            url: "https://github.com/ryanapierce",
            icon: "fa-github"
        }
    },

    // Project Links
    projects: {
        aboutMeChatbot: {
            title: "About Me Chatbot",
            url: "assets/projects/about-me-chat-bot/templates/ask_about_me_chat.html",
            github: "https://github.com/ryanapierce/about-me-chat-bot",
            image: "assets/images/openai.jpg"
        },
        pairTradingAlgorithm: {
            title: "Pair Trading Algorithm",
            url: "assets/projects/Mean_Reversion_Analysis_Project_ Milestone_1.pdf",
            github: "https://github.com/ryanapierce/pair-trading-algorithm",
            image: "assets/images/um.svg"
        }
    },

    // Copyright
    copyright: {
        year: new Date().getFullYear(),
        owner: "Ryan Pierce",
        template: "HTML5 UP",
        templateUrl: "https://html5up.net"
    }
};

// Make CONFIG available globally
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}