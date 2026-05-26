import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { MonitorPlay, Shield, ChevronRight, ChevronLeft, ChevronLeft, Play, X, Download, Mail, Loader2, ZoomIn, Cpu } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { useEffect, useMemo, useRef, useState } from "react";

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

const formatImagePath = (img) => {
  if (!img || String(img).trim() === "") return null;
  const v = String(img).trim();
  if (v.startsWith("http") || v.startsWith("data:") || v.startsWith("blob:")) return v;
  if (v.startsWith("/assets/")) return v;
  if (v.startsWith("/uploads/")) return `${API_BASE_URL}${v}`;
  if (v.startsWith("uploads/")) return `${API_BASE_URL}/${v}`;
  if (!v.includes("/")) return `${API_BASE_URL}/uploads/${v}`;
  return `${API_BASE_URL}/${v.replace(/^\/+/, "")}`;
};

const getYoutubeId = (url) => { const m = url.match(/(?:v=|youtu\.be\/)([^&?/]+)/); return m ? m[1] : null; };
const getEmbedUrl = (url) => {
  if (url.includes("youtube") || url.includes("youtu.be")) { const id = getYoutubeId(url); return id ? `https://www.youtube.com/embed/${id}?autoplay=1` : url; }
  if (url.includes("vimeo")) { const m = url.match(/vimeo\.com\/(\d+)/); return m ? `https://player.vimeo.com/video/${m[1]}?autoplay=1` : url; }
  return null;
};

const Reveal = ({ children, delay = 0 }) => {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const obs = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setVisible(true); obs.disconnect(); } }, { threshold: 0.1 });
    obs.observe(el); return () => obs.disconnect();
  }, []);
  return (
    <div ref={ref} className={`transition-all duration-700 ease-out ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`} style={{ transitionDelay: `${delay}ms` }}>
      {children}
    </div>
  );
};

const VideoModal = ({ url, onClose }) => {
  const embedUrl = getEmbedUrl(url);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" onClick={onClose}>
      <div className="relative w-full max-w-4xl mx-4" onClick={(e) => e.stopPropagation()}>
        <button onClick={onClose} className="absolute -top-10 right-0 text-white hover:text-[#c8a45d] flex items-center gap-2 text-sm"><X className="w-5 h-5" /> Close</button>
        {embedUrl ? (
          <iframe src={embedUrl} className="w-full aspect-video rounded-xl shadow-2xl" allow="autoplay; fullscreen" allowFullScreen title="Simulator Video" />
        ) : (
          <video src={formatImagePath(url)} controls autoPlay className="w-full aspect-video rounded-xl shadow-2xl" />
        )}
      </div>
    </div>
  );
};

const Lightbox = ({ images, index, onClose }) => {
  const [current, setCurrent] = useState(index);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm" onClick={onClose}>
      <div className="relative max-w-5xl w-full mx-4" onClick={(e) => e.stopPropagation()}>
        <button onClick={onClose} className="absolute -top-10 right-0 text-white hover:text-[#c8a45d] flex items-center gap-2 text-sm"><X className="w-5 h-5" /> Close</button>
        <img src={formatImagePath(images[current])} alt="" className="w-full max-h-[80vh] object-contain rounded-xl" />
        {images.length > 1 && (
          <div className="flex justify-center gap-2 mt-4">
            {images.map((_, i) => (
              <button key={i} onClick={() => setCurrent(i)} className={`w-2.5 h-2.5 rounded-full transition-all ${i === current ? "bg-[#c8a45d] scale-125" : "bg-white/40"}`} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const SimulatorCard = ({ item, reverse = false }) => {
  const [activeTab, setActiveTab] = useState("overview");
  const [videoModal, setVideoModal] = useState(null);
  const [lightbox, setLightbox] = useState(null);
  const [mainImage, setMainImage] = useState(0);

  const images = useMemo(() => {
    const raw = Array.isArray(item.images) && item.images.filter(Boolean).length > 0
      ? item.images.filter(Boolean)
      : item.image_url ? [item.image_url] : item.image ? [item.image] : [];
    return raw.map(formatImagePath).filter(Boolean);
  }, [item]);

  const videos = useMemo(() => (Array.isArray(item.videos) ? item.videos.filter(Boolean) : []), [item]);

  const specs = useMemo(() => {
    if (!item.specifications) return [];
    return item.specifications.split(/\n|(?=[•●▪◦])/).map(l => l.trim().replace(/^[•●▪◦\-]\s*/, "")).filter(Boolean);
  }, [item]);

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "specs", label: "Specifications" },
    ...(videos.length > 0 ? [{ id: "demo", label: "Demo Video" }] : []),
  ];

  return (
    <article className="bg-white border border-gray-100 shadow-sm hover:shadow-lg transition-shadow duration-300 overflow-hidden mb-1">

      {/* Header */}
      <div className="bg-gradient-to-r from-[#0d1f2d] to-[#1a3347] px-6 sm:px-10 py-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-xl sm:text-2xl font-bold text-white leading-tight">{item.name}</h3>
            {item.description && <p className="text-white/60 text-sm mt-1 max-w-xl line-clamp-1">{item.description}</p>}
          </div>
          <div className="flex gap-2 flex-shrink-0">
            <Link to="/enquiry" className="inline-flex items-center gap-1.5 text-xs font-semibold bg-[#c8a45d] hover:bg-[#b8944d] text-black px-4 py-2 rounded transition-colors">
              <Mail className="w-3.5 h-3.5" /> Enquiry
            </Link>
            {videos.length > 0 && (
              <button onClick={() => setVideoModal(videos[0])} className="inline-flex items-center gap-1.5 text-xs font-semibold bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded border border-white/20 transition-colors">
                <MonitorPlay className="w-3.5 h-3.5" /> Watch Demo
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className={`grid lg:grid-cols-2 gap-0 ${reverse ? "lg:[&>*:first-child]:order-2" : ""}`}>

        {/* LEFT — Gallery */}
        <div className="relative bg-[#f5f5f3] border-r border-gray-100">
          {images.length > 0 ? (
            <div>
              <div className="relative overflow-hidden cursor-zoom-in group" style={{ aspectRatio: "4/3" }} onClick={() => setLightbox(mainImage)}>
                <img
                  key={mainImage}
                  src={images[mainImage]}
                  alt={item.name}
                  className="w-full h-full object-contain p-6 transition-all duration-500 animate-fade"
                  onError={(e) => { e.currentTarget.parentElement.style.display = "none"; }}
                />

                {/* Left Arrow */}
                {images.length > 1 && (
                  <button
                    onClick={(e) => { e.stopPropagation(); setMainImage((p) => (p - 1 + images.length) % images.length); }}
                    className="absolute left-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-black/50 hover:bg-[#c8a45d] text-white rounded-full flex items-center justify-center transition-all opacity-0 group-hover:opacity-100 z-10 shadow-lg"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                )}

                {/* Right Arrow */}
                {images.length > 1 && (
                  <button
                    onClick={(e) => { e.stopPropagation(); setMainImage((p) => (p + 1) % images.length); }}
                    className="absolute right-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-black/50 hover:bg-[#c8a45d] text-white rounded-full flex items-center justify-center transition-all opacity-0 group-hover:opacity-100 z-10 shadow-lg"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                )}

                {/* Image counter */}
                {images.length > 1 && (
                  <div className="absolute top-3 left-3 bg-black/50 text-white text-xs px-2 py-1 rounded-full z-10">
                    {mainImage + 1} / {images.length}
                  </div>
                )}

                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors pointer-events-none" />

                {videos.length > 0 && (
                  <button onClick={(e) => { e.stopPropagation(); setVideoModal(videos[0]); }} className="absolute bottom-4 right-4 flex items-center gap-2 bg-black/70 hover:bg-[#c8a45d] text-white text-xs font-semibold px-3 py-2 rounded-full transition-all z-10">
                    <Play className="w-3.5 h-3.5 fill-current" /> Watch Demo
                  </button>
                )}
              </div>

              {images.length > 1 && (
                <div className="flex gap-2 p-3 bg-white border-t border-gray-100 overflow-x-auto scrollbar-hide">
                  {images.map((src, i) => (
                    <button key={i} onClick={() => setMainImage(i)} className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-all duration-300 ${i === mainImage ? "border-[#c8a45d] scale-105 shadow-md" : "border-gray-200 hover:border-[#c8a45d]/50 opacity-70 hover:opacity-100"}`}>
                      <img src={src} alt="" className="w-full h-full object-contain p-1" onError={(e) => { e.currentTarget.parentElement.style.display = "none"; }} />
                    </button>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center" style={{ aspectRatio: "4/3" }}>
              <div className="text-center text-gray-300">
                <Cpu className="w-16 h-16 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No image available</p>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT — Info */}
        <div className="flex flex-col">
          <div className="flex border-b border-gray-100 bg-gray-50/50">
            {tabs.map((tab) => (
              <button key={tab.id} onClick={() => setActiveTab(tab.id)} className={`flex-1 px-4 py-3 text-xs font-semibold uppercase tracking-wider transition-all border-b-2 ${activeTab === tab.id ? "border-[#c8a45d] text-[#0d1f2d] bg-white" : "border-transparent text-gray-400 hover:text-gray-600 hover:bg-gray-50"}`}>
                {tab.label}
              </button>
            ))}
          </div>

          <div className="flex-1 p-6 sm:p-8">
            {activeTab === "overview" && (
              <div className="space-y-5">
                {item.description && <p className="text-[15px] text-gray-600 leading-relaxed">{item.description}</p>}
                {specs.length > 0 && (
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-widest text-[#c8a45d] mb-3">Main Functions</h4>
                    <ul className="space-y-2">
                      {specs.slice(0, 5).map((s, i) => (
                        <li key={i} className="flex items-start gap-2.5 text-sm text-gray-600">
                          <span className="w-1.5 h-1.5 rounded-full bg-[#c8a45d] flex-shrink-0 mt-2" />{s}
                        </li>
                      ))}
                      {specs.length > 5 && <li><button onClick={() => setActiveTab("specs")} className="text-xs text-[#c8a45d] hover:underline font-medium">+{specs.length - 5} more →</button></li>}
                    </ul>
                  </div>
                )}
              </div>
            )}
            {activeTab === "specs" && (
              <div>
                <h4 className="text-xs font-bold uppercase tracking-widest text-[#c8a45d] mb-4">Technical Specifications</h4>
                {specs.length > 0 ? (
                  <ul className="space-y-2.5">
                    {specs.map((s, i) => (
                      <li key={i} className="flex items-start gap-3 text-sm text-gray-600 pb-2.5 border-b border-gray-50 last:border-0">
                        <ChevronRight className="w-4 h-4 text-[#c8a45d] flex-shrink-0 mt-0.5" />{s}
                      </li>
                    ))}
                  </ul>
                ) : <p className="text-gray-400 text-sm italic">No specifications available.</p>}
              </div>
            )}
            {activeTab === "demo" && videos.length > 0 && (
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-widest text-[#c8a45d] mb-4">Simulator Demo</h4>
                {videos.map((vid, i) => {
                  const ytId = getYoutubeId(vid);
                  return (
                    <button key={i} onClick={() => setVideoModal(vid)} className="w-full group relative rounded-lg overflow-hidden border border-gray-200 hover:border-[#c8a45d] transition-colors">
                      {ytId ? (
                        <img src={`https://img.youtube.com/vi/${ytId}/mqdefault.jpg`} alt="" className="w-full aspect-video object-cover group-hover:scale-105 transition-transform duration-300" />
                      ) : (
                        <div className="w-full aspect-video bg-[#0d1f2d] flex items-center justify-center"><MonitorPlay className="w-12 h-12 text-white/40" /></div>
                      )}
                      <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                        <div className="w-14 h-14 bg-[#c8a45d] rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                          <Play className="w-6 h-6 text-black fill-current ml-1" />
                        </div>
                      </div>
                      <p className="absolute bottom-3 left-3 text-white text-xs font-medium bg-black/60 px-2 py-1 rounded">Video {i + 1}</p>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          <div className="p-4 border-t border-gray-100 bg-gray-50/50 flex flex-wrap gap-2">
            <Link to="/enquiry" className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#0d1f2d] bg-[#c8a45d] hover:bg-[#b8944d] px-4 py-2.5 rounded transition-colors">
              <Mail className="w-3.5 h-3.5" /> Send Enquiry
            </Link>
          </div>
        </div>
      </div>

      {videoModal && <VideoModal url={videoModal} onClose={() => setVideoModal(null)} />}
      {lightbox !== null && <Lightbox images={images} index={lightbox} onClose={() => setLightbox(null)} />}
    </article>
  );
};

const SimulatorsPage = () => {
  const [simulators, setSimulators] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { window.scrollTo(0, 0); }, []);

  useEffect(() => {
    (async () => {
      try {
        const catRes = await fetch(`${API_BASE_URL}/api/product-categories`);
        const catData = await catRes.json();
        const simCat = (Array.isArray(catData) ? catData : []).find(c =>
          String(c.name || "").toLowerCase().includes("simulator")
        );
        if (!simCat) { setSimulators([]); setLoading(false); return; }
        const prodRes = await fetch(`${API_BASE_URL}/api/products?category_id=${simCat.id}&published=true`);
        const prodData = await prodRes.json();
        setSimulators(Array.isArray(prodData) ? prodData : []);
      } catch (err) {
        setError("Unable to load simulators right now.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="min-h-screen bg-[#f4f3ef]">
      <Header />
      <main>

        {/* HERO */}
        <section className="relative pt-32 pb-20 bg-gradient-to-br from-[#0d1f2d] via-[#1a3347] to-[#0d2a1e] overflow-hidden">
          <div className="absolute inset-0 opacity-5">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="absolute border border-white/20 rounded-full"
                style={{ width: `${(i + 1) * 200}px`, height: `${(i + 1) * 200}px`, top: "50%", left: "50%", transform: "translate(-50%,-50%)" }} />
            ))}
          </div>
          <div className="container-width px-4 sm:px-6 lg:px-8 relative">
            <div className="max-w-4xl">
              <div className="inline-flex items-center gap-2 bg-[#c8a45d]/20 border border-[#c8a45d]/30 text-[#c8a45d] text-xs font-semibold uppercase tracking-widest px-4 py-2 rounded-full mb-6">
                <MonitorPlay className="w-3.5 h-3.5" /> Training Systems
              </div>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                Simulators &<br /><span className="text-[#c8a45d]">Training Systems</span>
              </h1>
              <p className="text-lg text-white/70 max-w-2xl leading-relaxed mb-8">
                100% indigenously developed simulation platforms for modern defence readiness — enabling realistic training without operational risk.
              </p>
              <div className="flex flex-wrap gap-8">
                {[{ v: "100%", l: "Indigenous" }, { v: "ISO", l: "9001:2015" }, { v: "33+", l: "Years" }].map(s => (
                  <div key={s.l}>
                    <p className="text-3xl font-bold text-[#c8a45d]">{s.v}</p>
                    <p className="text-white/60 text-sm">{s.l}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* CONTENT */}
        <div className="container-width px-4 sm:px-6 lg:px-8 py-12">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-32 gap-4">
              <Loader2 className="w-10 h-10 animate-spin text-[#c8a45d]" />
              <p className="text-gray-400 text-sm">Loading simulators...</p>
            </div>
          ) : error ? (
            <div className="text-center py-20 text-red-500">{error}</div>
          ) : simulators.length === 0 ? (
            <div className="text-center py-20 text-gray-400">No simulators found.</div>
          ) : (
            <div className="space-y-6">
              {simulators.map((item, i) => (
                <Reveal key={item.id} delay={i * 80}>
                  <SimulatorCard item={item} reverse={i % 2 !== 0} />
                </Reveal>
              ))}
            </div>
          )}
        </div>

        {/* CTA */}
        <section className="bg-gradient-to-r from-[#0d1f2d] to-[#1a3347] py-16">
          <div className="container-width px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-4">Request a Live Demonstration</h2>
            <p className="text-white/70 mb-8 max-w-xl mx-auto">Experience our simulators firsthand. Contact our team to schedule a demo at your facility.</p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link to="/enquiry" className="inline-flex items-center gap-2 bg-[#c8a45d] hover:bg-[#b8944d] text-black font-bold px-8 py-3 rounded transition-all shadow-lg">
                <Mail className="w-4 h-4" /> Send Enquiry
              </Link>
              <Link to="/defence-systems" className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold px-8 py-3 rounded transition-all">
                Defence Systems <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </section>

      </main>
      <Footer />
    </div>
  );
};

export default SimulatorsPage;