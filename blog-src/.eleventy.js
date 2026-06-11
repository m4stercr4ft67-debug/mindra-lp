module.exports = function(eleventyConfig) {
  eleventyConfig.addFilter("formatDate", function(d) {
    const dt = d instanceof Date ? d : new Date(d);
    return dt.toLocaleDateString("pt-BR", { year:"numeric", month:"long", day:"numeric" });
  });
  eleventyConfig.addFilter("dateISO", function(d) {
    return (d instanceof Date ? d : new Date(d)).toISOString().split("T")[0];
  });
  eleventyConfig.addCollection("posts", function(api) {
    return api.getAll().filter(item => item.inputPath.includes("/posts/") && item.inputPath.endsWith(".md")).reverse();
  });
  return {
    dir: { input:"blog-src", output:"blog", includes:"_includes", data:"_data" },
    markdownTemplateEngine:"njk",
    htmlTemplateEngine:"njk"
  };
};
