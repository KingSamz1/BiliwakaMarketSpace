import streamlit as st
import base64
from database import get_connection, init_db
from utils import apply_theme, init_session_defaults, render_footer, render_topbar, guard_logged_in, render_carousel

st.set_page_config(page_title="MarketSpace - Biliwaka", page_icon="🏪", layout="wide")
init_session_defaults()
init_db()
apply_theme()
guard_logged_in()
render_topbar()

if "edit_ad_id" not in st.session_state: st.session_state.edit_ad_id = None
if "view_ad_id" not in st.session_state: st.session_state.view_ad_id = None
if "show_create_form" not in st.session_state: st.session_state.show_create_form = False
if "gallery_idx" not in st.session_state: st.session_state.gallery_idx = 0

with get_connection() as conn:
    vendor_banners = conn.execute("SELECT media FROM vendor_banners WHERE is_active = 1 AND (expires_at IS NULL OR expires_at >= date('now')) ORDER BY id DESC LIMIT 6").fetchall()
if vendor_banners:
    banner_urls = [b['media'] for b in vendor_banners if b['media'] and not b['media'].endswith('.mp4') and 'watch?v=' not in b['media']]
    if banner_urls: render_carousel(banner_urls, auto_slide=True, interval=5000); st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

col_search, col_cat = st.columns([3, 1])
with col_search: search = st.text_input("🔍 Search listings...", label_visibility="collapsed")
with col_cat: category_filter = st.selectbox("Category", ["All", "Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"], label_visibility="collapsed")

with get_connection() as conn:
    query = "SELECT a.*, u.full_name as seller_name FROM ads a JOIN users u ON u.id = a.user_id WHERE a.is_active = 1"
    params = []
    if search: query += " AND (a.title LIKE ? OR a.description LIKE ?)"; params.extend([f"%{search}%", f"%{search}%"])
    if category_filter != "All": query += " AND a.category LIKE ?"; params.append(f"%{category_filter}%")
    query += " ORDER BY a.is_featured DESC, a.clicks DESC"
    listings = conn.execute(query, params).fetchall()

btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1: 
    if st.button("➕ New", type="primary", use_container_width=True): st.switch_page("pages/2_📊_Dashboard.py")
with btn_col2: st.subheader(f"📢 Available Listings ({len(listings)})")

# --- VIEW MODAL ---
if st.session_state.view_ad_id is not None:
    st.markdown("---")
    with get_connection() as conn:
        ad = conn.execute("SELECT a.*, u.full_name, u.phone FROM ads a JOIN users u ON u.id = a.user_id WHERE a.id = ?", (st.session_state.view_ad_id,)).fetchone()
        conn.execute("UPDATE ads SET clicks = clicks + 1 WHERE id = ?", (st.session_state.view_ad_id,))
        similar = conn.execute("SELECT * FROM ads WHERE category = ? AND id != ? AND is_active = 1 LIMIT 4", (ad['category'], ad['id'])).fetchall()
        also_viewed = conn.execute("SELECT * FROM ads WHERE id != ? AND is_active = 1 ORDER BY RANDOM() LIMIT 4", (ad['id'],)).fetchall()

    images = [m.strip() for m in ad['media'].split(',') if m.strip()] if ad['media'] else []
    valid_images = [img for img in images if 'watch?v=' not in img and (img.startswith('http') or img.startswith('data:'))]
    
    if valid_images:
        st.session_state.gallery_idx = st.session_state.get("gallery_idx", 0) % len(valid_images)
        current_img = valid_images[st.session_state.gallery_idx]
        
        c_img, c_info = st.columns([1.5, 1])
        with c_img:
            if current_img.endswith('.mp4'): st.video(current_img)
            else: st.image(current_img, use_container_width=True)
            gc1, gc2, gc3 = st.columns([1, 6, 1])
            with gc1:
                if st.button("◀", key="g_prev"): st.session_state.gallery_idx = (st.session_state.gallery_idx - 1) % len(valid_images); st.rerun()
            with gc3:
                if st.button("▶", key="g_next"): st.session_state.gallery_idx = (st.session_state.gallery_idx + 1) % len(valid_images); st.rerun()
            with gc2:
                st.markdown(f"<div style='text-align:center;color:#94a3b8;font-size:0.9rem;'>Image {st.session_state.gallery_idx + 1} of {len(valid_images)}</div>", unsafe_allow_html=True)
        with c_info:
            st.markdown(f"### {ad['title']}")
            if ad['discount'] > 0:
                sp = ad['price'] - (ad['price'] * (ad['discount'] / 100))
                st.markdown(f"~~UGX {ad['price']:,.0f}~~ -> **<span style='color:#ef4444;'>UGX {sp:,.0f}</span>**", unsafe_allow_html=True)
            else: st.markdown(f"**<span style='color:#fbbf24;font-size:1.5rem;'>UGX {ad['price']:,.0f}</span>**", unsafe_allow_html=True)
            st.write(f"📁 {ad['category']} | 🏢 {ad['full_name']}")
            st.write(ad['description'])
            ad_phone = str(ad['phone']).strip()
            if ad_phone.startswith("0"): ad_phone = "256" + ad_phone[1:]
            st.markdown(f"<a href='https://wa.me/{ad_phone}?text=Hello%20I%20am%20interested%20in%20*{ad['title']}*' target='_blank' style='display:inline-block;padding:12px;background:#25D366;color:white;border-radius:8px;text-decoration:none;font-weight:700;'>💬 Chat on WhatsApp</a>", unsafe_allow_html=True)

    if similar:
        st.subheader("🏷️ Similar Products")
        sc = st.columns(4)
        for i, s in enumerate(similar):
            with sc[i]:
                if st.button(f"{s['title']}", key=f"sim_{s['id']}", use_container_width=True): st.session_state.view_ad_id = s['id']; st.rerun()
    if also_viewed:
        st.subheader("👀 Customers Also Viewed")
        vc = st.columns(4)
        for i, v in enumerate(also_viewed):
            with vc[i]:
                if st.button(f"{v['title']}", key=f"v_{v['id']}", use_container_width=True): st.session_state.view_ad_id = v['id']; st.rerun()

    if st.button("← Back to Listings", use_container_width=True): st.session_state.view_ad_id = None; st.rerun()

# --- EDIT MODAL ---
if st.session_state.edit_ad_id is not None:
    st.markdown("---")
    st.subheader("✏️ Edit Listing")
    edit_id = st.session_state.edit_ad_id
    with get_connection() as conn: ad = conn.execute("SELECT * FROM ads WHERE id = ?", (edit_id,)).fetchone()
    if ad:
        with st.form("edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_title = st.text_input("Title", value=ad['title'])
                new_cat = st.selectbox("Category", ["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"], index=["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"].index(ad['category']) if ad['category'] in ["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"] else 0)
                new_price = st.number_input("Price", value=ad['price'])
                new_phone = st.text_input("Listing Phone", value=ad['phone'])
            with c2:
                new_desc = st.text_area("Desc", value=ad['description'], height=120)
                new_discount = st.number_input("Discount %", min_value=0.0, max_value=90.0, value=float(ad['discount']), step=5.0)
            st.markdown("**📸 Image URLs (Max 10, one per line)**")
            existing = ad['media'].split(',') if ad['media'] else []
            new_img = st.text_area("URLs", value="\n".join(existing), height=100)
            cs, cc = st.columns(2)
            with cs:
                if st.form_submit_button("💾 Save", use_container_width=True):
                    imgs = [u.strip() for u in new_img.split('\n') if u.strip()][:10]
                    with get_connection() as conn: conn.execute("UPDATE ads SET title=?, category=?, price=?, description=?, media=?, discount=?, phone=? WHERE id=?", (new_title, new_cat, new_price, new_desc, ",".join(imgs), new_discount, new_phone, edit_id))
                    st.session_state.edit_ad_id = None; st.success("Updated!"); st.rerun()
            with cc:
                if st.form_submit_button("❌ Cancel", use_container_width=True): st.session_state.edit_ad_id = None; st.rerun()

# --- GRID ---
if not listings: st.info("No listings found.")
else:
    cols = st.columns(3)
    for i, row in enumerate(listings):
        with cols[i % 3]:
            list_phone = str(row['phone']).strip()
            if list_phone.startswith("0"): list_phone = "256" + list_phone[1:]
            images = [m.strip() for m in row['media'].split(',') if m.strip()] if row['media'] else []
            valid_images = [img for img in images if 'watch?v=' not in img and (img.startswith('http') or img.startswith('data:'))]
            first_image = valid_images[0] if valid_images else ""
            
            media_html = ""
            if first_image:
                if first_image.endswith('.mp4'): media_html = f'<video style="width:100%;height:180px;object-fit:cover;border-radius:10px 10px 0 0;" controls><source src="{first_image}" type="video/mp4"></video>'
                else: media_html = f'<img src="{first_image}" style="width:100%;height:180px;object-fit:cover;border-radius:10px 10px 0 0;">'
            
            feat = '<div style="position:absolute;top:10px;left:10px;background:#f59e0b;color:#000;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:800;">⭐ FEATURED</div>' if row['is_featured'] else ""
            sale = ""
            if row['discount'] > 0:
                sp = row['price'] - (row['price'] * (row['discount'] / 100))
                sale = f'<div style="position:absolute;top:10px;right:10px;background:#ef4444;color:white;padding:4px 10px;border-radius:20px;font-size:0.7rem;font-weight:800;">-{row["discount"]}%</div><div style="position:absolute;bottom:190px;right:10px;background:#111827;color:#25D366;padding:4px 10px;border-radius:8px;font-size:0.75rem;font-weight:700;">UGX {sp:,.0f}</div>'
            
            gal = f'<div style="position:absolute;bottom:190px;right:80px;background:rgba(0,0,0,0.7);color:white;padding:2px 8px;border-radius:4px;font-size:0.7rem;">📸 {len(valid_images)}</div>' if len(valid_images) > 1 else ""

            st.markdown(f"""
            <div style="background:#111827;border-radius:12px;border:1px solid #1f2937;overflow:hidden;margin-bottom:1.5rem;position:relative;">
                {feat}{sale}{gal}{media_html}
                <div style="padding:1rem;">
                    <h3 style="margin:0 0 0.3rem;color:#e5e7eb;font-size:1rem;">{row['title']}</h3>
                    <p style="color:#94a3b8;font-size:0.8rem;margin:0 0 0.5rem;">📁 {row['category']} | 🏢 {row['seller_name']}</p>
                    <p style="color:#fbbf24;font-weight:800;font-size:1.1rem;margin:0 0 0.8rem;">UGX {row['price']:,.0f}</p>
                    <div style="display:flex;gap:6px;">
                        <a href="https://wa.me/{list_phone}?text=Hello%20I%20am%20interested%20in%20*{row['title']}*" target="_blank" style="flex:1;text-align:center;padding:8px;background:#25D366;color:white;border-radius:6px;text-decoration:none;font-weight:600;">💬</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_view, col_edit = st.columns(2)
            with col_view:
                if st.button("👁 View", key=f"view_{row['id']}", use_container_width=True):
                    st.session_state.view_ad_id = row['id']; st.session_state.gallery_idx = 0; st.rerun()
            with col_edit:
                if st.session_state.user['id'] == row['user_id']:
                    if st.button("✏️ Edit", key=f"edit_{row['id']}", use_container_width=True):
                        st.session_state.edit_ad_id = row['id']; st.rerun()

render_footer()
