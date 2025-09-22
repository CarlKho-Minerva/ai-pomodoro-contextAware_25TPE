const fs = require('fs');
const path = require('path');

/**
 * Build script for the Pomodoro Work Journal website
 * Processes both blog posts and pomodoro session logs
 */

// Configuration
const CONTENT_DIRS = {
    blogs: './content/blogs',
    pomodoros: './content/pomodoros'
};
const TEMPLATE_PATH = './src/index-template.html';
const OUTPUT_PATH = './dist/index.html';

/**
 * Process markdown files from a directory and convert to HTML
 * @param {string} sourceDir - Directory containing markdown files
 * @returns {string} Combined HTML string
 */
function processMarkdownFiles(sourceDir) {
    try {
        if (!fs.existsSync(sourceDir)) {
            console.log(`Directory ${sourceDir} does not exist, skipping...`);
            return '';
        }

        // Read all .md files from the directory
        const files = fs.readdirSync(sourceDir)
            .filter(file => file.endsWith('.md'))
            .sort((a, b) => b.localeCompare(a)); // Reverse chronological order

        if (files.length === 0) {
            console.log(`No markdown files found in ${sourceDir}`);
            return '';
        }

        // Process each file
        const htmlParts = files.map(filename => {
            const filePath = path.join(sourceDir, filename);
            const content = fs.readFileSync(filePath, 'utf-8');

            // Simple markdown to HTML conversion
            // This is a basic implementation - for production, consider using a proper markdown parser
            let html = content
                // Convert headings
                .replace(/^# (.*$)/gim, '<h1>$1</h1>')
                .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                .replace(/^### (.*$)/gim, '<h3>$1</h3>')
                // Convert bold and italic
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                // Convert links
                .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
                // Convert line breaks to paragraphs
                .split('\n\n')
                .map(paragraph => {
                    if (paragraph.trim()) {
                        // Handle lists
                        if (paragraph.trim().startsWith('- ')) {
                            const listItems = paragraph.split('\n')
                                .filter(line => line.trim().startsWith('- '))
                                .map(line => `<li>${line.replace(/^- /, '')}</li>`)
                                .join('');
                            return `<ul>${listItems}</ul>`;
                        }
                        // Handle details tags (already HTML)
                        if (paragraph.trim().startsWith('<details>')) {
                            return paragraph;
                        }
                        // Regular paragraphs
                        if (!paragraph.includes('<h') && !paragraph.includes('<ul>')) {
                            return `<p>${paragraph}</p>`;
                        }
                        return paragraph;
                    }
                    return '';
                })
                .filter(p => p)
                .join('\n');

            // Wrap in a container div
            const containerClass = sourceDir.includes('pomodoros') ? 'pomodoro-card' : 'blog-post';
            return `<div class="${containerClass}">\n${html}\n</div>`;
        });

        return htmlParts.join('\n\n');
    } catch (error) {
        console.error(`Error processing ${sourceDir}:`, error);
        return '';
    }
}

/**
 * Main build function
 */
function build() {
    try {
        console.log('Starting website build...');

        // Read the HTML template
        if (!fs.existsSync(TEMPLATE_PATH)) {
            throw new Error(`Template file ${TEMPLATE_PATH} not found`);
        }

        let template = fs.readFileSync(TEMPLATE_PATH, 'utf-8');

        // Process blog posts
        console.log('Processing blog posts...');
        const blogHtml = processMarkdownFiles(CONTENT_DIRS.blogs);

        // Process pomodoro entries
        console.log('Processing pomodoro entries...');
        const pomodoroHtml = processMarkdownFiles(CONTENT_DIRS.pomodoros);

        // Replace placeholders in template
        template = template.replace('<!--BLOG_POSTS-->', blogHtml);
        template = template.replace('<!--POMODORO_FEED-->', pomodoroHtml);

        // Ensure output directory exists
        const outputDir = path.dirname(OUTPUT_PATH);
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        // Copy CSS files to dist
        const cssSourceDir = './src/css';
        const cssDestDir = './dist/css';
        if (fs.existsSync(cssSourceDir)) {
            if (!fs.existsSync(cssDestDir)) {
                fs.mkdirSync(cssDestDir, { recursive: true });
            }
            const cssFiles = fs.readdirSync(cssSourceDir).filter(file => file.endsWith('.css'));
            cssFiles.forEach(file => {
                fs.copyFileSync(path.join(cssSourceDir, file), path.join(cssDestDir, file));
            });
            console.log(`Copied ${cssFiles.length} CSS files`);
        }

        // Write the final HTML file
        fs.writeFileSync(OUTPUT_PATH, template, 'utf-8');

        console.log(`Build complete! Generated ${OUTPUT_PATH}`);
        console.log(`- Blog posts: ${blogHtml ? 'Found content' : 'No content'}`);
        console.log(`- Pomodoro entries: ${pomodoroHtml ? 'Found content' : 'No content'}`);

    } catch (error) {
        console.error('Build failed:', error);
        process.exit(1);
    }
}

// Run the build
if (require.main === module) {
    build();
}

module.exports = { build, processMarkdownFiles };