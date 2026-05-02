// Sample data
const storiesData = [
    { username: 'You', avatar: '+', isYour: true },
    { username: 'sarah_codes', avatar: 'SC' },
    { username: 'design_mike', avatar: 'DM' },
    { username: 'data_anna', avatar: 'DA' },
    { username: 'photo_emily', avatar: 'PE' },
    { username: 'music_alex', avatar: 'MA' },
    { username: 'cook_maria', avatar: 'CM' }
];

const postsData = [
    {
        id: 1,
        username: 'sarah_codes',
        userAvatar: 'SC',
        skill: 'React Development',
        content: '🚀',
        caption: 'Just finished my React project! Built a complete e-commerce app with hooks and context API. The journey was challenging but so rewarding!',
        tags: '#react #javascript #webdev #coding',
        likes: 245,
        comments: 18,
        time: '2 hours ago',
        trending: true,
        liked: false,
        bookmarked: false
    },
    {
        id: 2,
        username: 'design_mike',
        userAvatar: 'DM',
        skill: 'UI/UX Design',
        content: '🎨',
        caption: 'New design system completed! Working on accessibility and inclusive design principles. What do you think about these color combinations?',
        tags: '#design #uiux #accessibility #designsystem',
        likes: 189,
        comments: 31,
        time: '4 hours ago',
        trending: false,
        liked: true,
        bookmarked: false
    },
    {
        id: 3,
        username: 'data_anna',
        userAvatar: 'DA',
        skill: 'Data Science',
        content: '📊',
        caption: 'Analyzed customer behavior data and found some fascinating patterns! Machine learning is opening up so many possibilities.',
        tags: '#datascience #python #ml #analytics',
        likes: 156,
        comments: 24,
        time: '6 hours ago',
        trending: true,
        liked: false,
        bookmarked: true
    },
    {
        id: 4,
        username: 'photo_emily',
        userAvatar: 'PE',
        skill: 'Photography',
        content: '📸',
        caption: 'Golden hour magic! Learning about natural lighting has completely transformed my portrait photography. Practice makes perfect!',
        tags: '#photography #portraits #goldenhour #learning',
        likes: 298,
        comments: 42,
        time: '8 hours ago',
        trending: false,
        liked: true,
        bookmarked: false
    }
];

const trendingSkillsData = [
    { name: 'React Development', icon: '⚛️', stats: '2.1k learning' },
    { name: 'Digital Marketing', icon: '📱', stats: '1.8k learning' },
    { name: 'Data Science', icon: '📊', stats: '1.5k learning' },
    { name: 'UI/UX Design', icon: '🎨', stats: '1.3k learning' }
];

const suggestionsData = [
    { name: 'Alex Thompson', avatar: 'AT', skill: 'JavaScript Expert', followed: false },
    { name: 'Lisa Chen', avatar: 'LC', skill: 'Marketing Guru', followed: false },
    { name: 'Carlos Rodriguez', avatar: 'CR', skill: 'Python Developer', followed: false },
    { name: 'Emma Wilson', avatar: 'EW', skill: 'Designer', followed: false }
];

const yourLearningData = [
    { name: 'Advanced JavaScript', icon: '🟨', progress: '65% complete' },
    { name: 'Photography Basics', icon: '📸', progress: '30% complete' },
    { name: 'Spanish Conversation', icon: '🇪🇸', progress: '85% complete' }
];

// Create stories
function createStory(story) {
    return `
        <div class="story-item" onclick="viewStory('${story.username}')">
            <div class="story-avatar">
                <div class="story-avatar-inner">${story.avatar}</div>
            </div>
            <div class="story-username">${story.username}</div>
        </div>
    `;
}

// Create posts
function createPost(post) {
    return `
        <div class="post fade-in">
            <div class="post-header">
                <div class="post-user">
                    <div class="post-avatar">${post.userAvatar}</div>
                    <div class="post-info">
                        <div class="post-username">${post.username}</div>
                        <div class="post-skill">${post.skill}</div>
                    </div>
                </div>
                <div class="post-menu">⋯</div>
            </div>
            <div class="post-content">
                <div class="post-image">
                    ${post.content}
                    ${post.trending ? '<div class="trending-badge">🔥 Trending</div>' : ''}
                </div>
            </div>
            <div class="post-actions">
                <button class="action-btn ${post.liked ? 'liked' : ''}" onclick="toggleLike(${post.id})">
                    ${post.liked ? '❤️' : '🤍'}
                </button>
                <button class="action-btn" onclick="comment(${post.id})">💬</button>
                <button class="action-btn" onclick="share(${post.id})">📤</button>
                <button class="action-btn ${post.bookmarked ? 'bookmarked' : ''}" onclick="toggleBookmark(${post.id})" style="margin-left: auto;">
                    ${post.bookmarked ? '🔖' : '📌'}
                </button>
            </div>
            <div class="post-stats">${post.likes.toLocaleString()} likes</div>
            <div class="post-caption">
                <strong>${post.username}</strong> ${post.caption} <span class="post-tags">${post.tags}</span>
            </div>
            <div class="post-comments">View all ${post.comments} comments</div>
            <div class="post-time">${post.time}</div>
        </div>
    `;
}

// Create trending skill
function createTrendingSkill(skill) {
    return `
        <div class="trending-item" onclick="exploreSkill('${skill.name}')">
            <div class="trending-icon">${skill.icon}</div>
            <div class="trending-info">
                <div class="trending-name">${skill.name}</div>
                <div class="trending-stats">${skill.stats}</div>
            </div>
        </div>
    `;
}

// Create suggestion
function createSuggestion(suggestion) {
    return `
        <div class="suggestion-item">
            <div class="suggestion-avatar">${suggestion.avatar}</div>
            <div class="suggestion-info">
                <div class="suggestion-name">${suggestion.name}</div>
                <div class="suggestion-skill">${suggestion.skill}</div>
            </div>
            <button class="follow-btn" onclick="followUser('${suggestion.name}')" 
                    id="follow-${suggestion.name.replace(' ', '-')}">
                Follow
            </button>
        </div>
    `;
}

// Create learning item
function createLearningItem(item) {
    return `
        <div class="trending-item" onclick="continueClass('${item.name}')">
            <div class="trending-icon">${item.icon}</div>
            <div class="trending-info">
                <div class="trending-name">${item.name}</div>
                <div class="trending-stats">${item.progress}</div>
            </div>
        </div>
    `;
}

// Event handlers
function viewStory(username) {
    console.log('Viewing story:', username);
}

function toggleLike(postId) {
    const post = postsData.find(p => p.id === postId);
    post.liked = !post.liked;
    post.likes += post.liked ? 1 : -1;
    renderFeed();
}

function toggleBookmark(postId) {
    const post = postsData.find(p => p.id === postId);
    post.bookmarked = !post.bookmarked;
    renderFeed();
}

function comment(postId) {
    console.log('Commenting on post:', postId);
}

function share(postId) {
    console.log('Sharing post:', postId);
}

function followUser(userName) {
    const btn = document.getElementById(`follow-${userName.replace(' ', '-')}`);
    btn.textContent = 'Following';
    btn.style.background = '#10b981';
    setTimeout(() => {
        btn.textContent = 'Follow';
        btn.style.background = '#667eea';
    }, 2000);
}

function exploreSkill(skillName) {
    console.log('Exploring skill:', skillName);
}

function continueClass(className) {
    console.log('Continuing class:', className);
}

// Render functions
function renderStories() {
    document.getElementById('storiesContainer').innerHTML = 
        storiesData.map(createStory).join('');
}

function renderFeed() {
    document.getElementById('feedContainer').innerHTML = 
        postsData.map(createPost).join('');
}

function renderSidebar() {
    document.getElementById('trendingSkills').innerHTML = 
        trendingSkillsData.map(createTrendingSkill).join('');
    
    document.getElementById('suggestions').innerHTML = 
        suggestionsData.map(createSuggestion).join('');
    
    document.getElementById('yourLearning').innerHTML = 
        yourLearningData.map(createLearningItem).join('');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    renderStories();
    renderFeed();
    renderSidebar();
});

// Infinite scroll
let isLoading = false;

window.addEventListener('scroll', () => {
    if (isLoading) return;
    
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
        loadMorePosts();
    }
});

function loadMorePosts() {
    isLoading = true;
    document.getElementById('loadingIndicator').style.display = 'block';
    
    // Simulate API call
    setTimeout(() => {
        // Add more posts (in real app, fetch from API)
        const newPosts = [
            {
                id: postsData.length + 1,
                username: 'music_alex',
                userAvatar: 'MA',
                skill: 'Music Production',
                content: '🎵',
                caption: 'Beat making session! Learning about sound design and mixing. The creative process never gets old.',
                tags: '#music #production #beats #creative',
                likes: 87,
                comments: 12,
                time: '12 hours ago',
                trending: false,
                liked: false,
                bookmarked: false
            }
        ];
        
        postsData.push(...newPosts);
        renderFeed();
        
        document.getElementById('loadingIndicator').style.display = 'none';
        isLoading = false;
    }, 1500);
}

// Search functionality
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value;
        if (query.length > 2) {
            console.log('Searching for:', query);
            // Implement search functionality
        }
    });
}