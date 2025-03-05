document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const sortOption = document.getElementById('sort-option');
    const requestCards = document.querySelectorAll('.request-card');
    const requestList = document.querySelector('.row');

    // Jika elemen .row tidak ditemukan, hentikan eksekusi
    if (!requestList) {
        console.error('Elemen .row tidak ditemukan di DOM.');
        return;
    }

    // Fungsi untuk memfilter dan mengurutkan permintaan
    function filterAndSortRequests() {
        const searchQuery = searchInput.value.toLowerCase();
        const selectedStatus = statusFilter.value;
        const sortOrder = sortOption.value;

        requestCards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();
            const status = card.querySelector('.request-status').textContent.toLowerCase();
            const dateSubmitted = card.querySelector('.request-date').textContent;

            // Filter berdasarkan pencarian dan status
            const matchesSearch = title.includes(searchQuery);
            const matchesStatus = selectedStatus === 'all' || status === selectedStatus;

            if (matchesSearch && matchesStatus) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });

        // Urutkan berdasarkan tanggal
        const visibleCards = Array.from(requestCards).filter(card => card.style.display !== 'none');
        visibleCards.sort((a, b) => {
            const dateA = new Date(a.querySelector('.request-date').textContent);
            const dateB = new Date(b.querySelector('.request-date').textContent);

            if (sortOrder === 'dateAsc') {
                return dateA - dateB; // Urutan terlama ke terbaru
            } else {
                return dateB - dateA; // Urutan terbaru ke terlama
            }
        });

        // Render ulang kartu yang sudah diurutkan
        requestList.innerHTML = ''; // Kosongkan konten
        visibleCards.forEach(card => requestList.appendChild(card));
    }

    // Tambahkan event listener untuk input pencarian, filter status, dan pengurutan
    searchInput.addEventListener('input', filterAndSortRequests);
    statusFilter.addEventListener('change', filterAndSortRequests);
    sortOption.addEventListener('change', filterAndSortRequests);
});